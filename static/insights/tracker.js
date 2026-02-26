/**
 * Insights behavior tracker: page_view, scroll_depth, click, page_exit, rage_click.
 * Uses sendBeacon to POST to collect endpoint. Respects consent and DNT when configured.
 */
(function () {
  'use strict';

  var COOKIE_SESS = 'ins_sess';
  var COOKIE_CID = 'ins_cid';
  var COOKIE_CONSENT = 'insights_consent';
  var SESS_DAYS = 30;
  var CID_DAYS = 365;
  var COLLECT_URL = window.INSIGHTS_COLLECT_URL || '/insights/collect/';
  var MAX_EVENTS_BATCH = 20;
  var SCROLL_MILESTONES = [25, 50, 75, 90];
  var RAGE_CLICK_THRESHOLD = 3;
  var RAGE_CLICK_WINDOW_MS = 1000;
  var TEXT_SNIPPET_MAX = 80;

  function getConfig() {
    return {
      requireConsent: (window.INSIGHTS_REQUIRE_CONSENT !== undefined ? window.INSIGHTS_REQUIRE_CONSENT : true),
      respectDnt: (window.INSIGHTS_RESPECT_DNT !== undefined ? window.INSIGHTS_RESPECT_DNT : false),
    };
  }

  function getCookie(name) {
    var m = document.cookie.match(new RegExp('(?:^|; )' + name.replace(/([.*+?^${}()|[\]\\])/g, '\\$1') + '=([^;]*)'));
    return m ? decodeURIComponent(m[1]) : null;
  }

  function setCookie(name, value, days) {
    var d = new Date();
    d.setTime(d.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = name + '=' + encodeURIComponent(value) + '; path=/; max-age=' + (days * 24 * 60 * 60) + '; SameSite=Lax';
  }

  function getOrCreateSid() {
    var s = getCookie(COOKIE_SESS);
    if (s) return s;
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      var r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
    setCookie(COOKIE_SESS, uuid, SESS_DAYS);
    return uuid;
  }

  function getOrCreateCid() {
    var c = getCookie(COOKIE_CID);
    if (c) return c;
    c = 'c' + Date.now() + '.' + Math.random().toString(36).slice(2, 12);
    setCookie(COOKIE_CID, c, CID_DAYS);
    return c;
  }

  function hasConsent() {
    var config = getConfig();
    if (config.requireConsent) {
      var v = getCookie(COOKIE_CONSENT);
      return v === '1' || v === 'true' || v === 'accepted';
    }
    return true;
  }

  function shouldTrack() {
    var config = getConfig();
    if (config.respectDnt && navigator.doNotTrack === '1') return false;
    return hasConsent();
  }

  var eventQueue = [];
  var scrollMaxPct = 0;
  var scrollMilestonesSent = {};
  var pageLoadTime = Date.now();
  var clickCountByTarget = {};
  var clickTimeByTarget = {};

  function enqueue(type, url, payload) {
    if (!shouldTrack()) return;
    eventQueue.push({
      type: type,
      url: url || (typeof location !== 'undefined' ? location.href : ''),
      ts: new Date().toISOString(),
      ref: typeof document !== 'undefined' && document.referrer ? document.referrer : '',
      payload: payload || {},
    });
  }

  function flush() {
    if (eventQueue.length === 0) return;
    var batch = eventQueue.splice(0, MAX_EVENTS_BATCH);
    var sid = getOrCreateSid();
    var cid = getOrCreateCid();
    var body = JSON.stringify({
      sid: sid,
      cid: cid,
      consent: hasConsent(),
      events: batch,
    });
    if (navigator.sendBeacon) {
      navigator.sendBeacon(COLLECT_URL, new Blob([body], { type: 'application/json' }));
    } else {
      var xhr = new XMLHttpRequest();
      xhr.open('POST', COLLECT_URL, true);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.send(body);
    }
  }

  function getClickPayload(el) {
    var tag = el ? (el.tagName || '').toLowerCase() : '';
    var id = (el && el.id) ? String(el.id).slice(0, 100) : '';
    var cls = (el && el.className && typeof el.className === 'string') ? String(el.className).slice(0, 200) : '';
    var dataTrack = (el && el.getAttribute && el.getAttribute('data-track')) ? String(el.getAttribute('data-track')).slice(0, 200) : '';
    var text = '';
    if (el && (el.innerText || el.textContent)) {
      text = String(el.innerText || el.textContent).replace(/\s+/g, ' ').trim().slice(0, TEXT_SNIPPET_MAX);
    }
    var href = (el && el.getAttribute && el.getAttribute('href')) ? String(el.getAttribute('href')).slice(0, 500) : '';
    return { tag: tag, id: id, class: cls, data_track: dataTrack, text: text, href: href };
  }

  function onPageView() {
    enqueue('page_view', location.href, {});
    flush();
  }

  function onScroll() {
    if (typeof document === 'undefined' || !document.documentElement || !document.body) return;
    var doc = document.documentElement;
    var scrollTop = window.pageYOffset || doc.scrollTop;
    var scrollHeight = (doc.scrollHeight || doc.offsetHeight) - (window.innerHeight || doc.clientHeight);
    if (scrollHeight <= 0) return;
    var pct = Math.min(100, Math.round((scrollTop / scrollHeight) * 100));
    if (pct > scrollMaxPct) scrollMaxPct = pct;
    for (var i = 0; i < SCROLL_MILESTONES.length; i++) {
      var m = SCROLL_MILESTONES[i];
      if (pct >= m && !scrollMilestonesSent[m]) {
        scrollMilestonesSent[m] = true;
        enqueue('scroll_depth', location.href, { milestone: m, max_scroll_pct: scrollMaxPct });
      }
    }
  }

  var scrollThrottle = null;
  function onScrollThrottled() {
    if (scrollThrottle) return;
    scrollThrottle = setTimeout(function () {
      scrollThrottle = null;
      onScroll();
    }, 150);
  }

  function isTrackableClick(el) {
    if (!el) return false;
    if (el.getAttribute && el.getAttribute('data-track')) return true;
    var tag = (el.tagName || '').toLowerCase();
    if (tag === 'a' || tag === 'button') return true;
    if (tag === 'input' && (el.type === 'submit' || el.type === 'button')) return true;
    return false;
  }

  function getTargetKey(el) {
    if (!el) return '';
    return (el.id || '') + '|' + (el.className || '') + '|' + (el.getAttribute && el.getAttribute('data-track') || '') + '|' + (el.tagName || '');
  }

  function onClick(e) {
    var el = e.target;
    while (el && el !== document.body && !isTrackableClick(el)) el = el.parentElement;
    if (!el || !isTrackableClick(el)) return;
    var key = getTargetKey(el);
    var now = Date.now();
    var count = (clickCountByTarget[key] || 0) + 1;
    var firstTime = clickTimeByTarget[key];
    if (!firstTime) clickTimeByTarget[key] = now;
    if (now - (firstTime || now) > RAGE_CLICK_WINDOW_MS) {
      clickCountByTarget[key] = 1;
      clickTimeByTarget[key] = now;
      count = 1;
    } else {
      clickCountByTarget[key] = count;
    }
    if (count >= RAGE_CLICK_THRESHOLD) {
      enqueue('rage_click', location.href, getClickPayload(el));
      clickCountByTarget[key] = 0;
      clickTimeByTarget[key] = 0;
    } else {
      enqueue('click', location.href, getClickPayload(el));
    }
    flush();
  }

  function onPageExit() {
    var timeOnPage = Date.now() - pageLoadTime;
    enqueue('page_exit', location.href, { time_on_page_ms: timeOnPage });
    flush();
  }

  function init() {
    if (!shouldTrack()) return;
    onPageView();
    if (typeof document !== 'undefined') {
      document.addEventListener('scroll', onScrollThrottled, { passive: true });
      document.addEventListener('click', onClick, true);
      document.addEventListener('visibilitychange', function () {
        if (document.visibilityState === 'hidden') onPageExit();
      });
      window.addEventListener('pagehide', onPageExit);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.InsightsTracker = {
    setConsent: function (accepted) {
      setCookie(COOKIE_CONSENT, accepted ? '1' : '0', 365);
    },
    flush: flush,
    hasConsent: hasConsent,
    shouldTrack: shouldTrack,
  };
})();
