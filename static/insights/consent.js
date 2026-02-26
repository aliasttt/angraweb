/**
 * Minimal consent banner: show if no consent cookie; Accept / Reject set cookie and hide.
 * Call InsightsTracker.setConsent(true/false). If rejected, tracker stops (no new events).
 */
(function () {
  'use strict';
  var COOKIE_CONSENT = 'insights_consent';
  var BANNER_ID = 'insights-consent-banner';

  function getCookie(name) {
    var m = document.cookie.match(new RegExp('(?:^|; )' + name.replace(/([.*+?^${}()|[\]\\])/g, '\\$1') + '=([^;]*)'));
    return m ? decodeURIComponent(m[1]) : null;
  }

  function setCookie(name, value, days) {
    var maxAge = days * 24 * 60 * 60;
    document.cookie = name + '=' + encodeURIComponent(value) + '; path=/; max-age=' + maxAge + '; SameSite=Lax';
  }

  function showBannerIfNeeded() {
    if (getCookie(COOKIE_CONSENT) !== null) return;
    var requireConsent = (window.INSIGHTS_REQUIRE_CONSENT !== undefined ? window.INSIGHTS_REQUIRE_CONSENT : true);
    if (!requireConsent) return;

    var banner = document.getElementById(BANNER_ID);
    if (banner) return;

    var text = window.INSIGHTS_CONSENT_MESSAGE || 'We use cookies to improve your experience and analyze site usage.';
    var privacyUrl = window.INSIGHTS_PRIVACY_URL || '/privacy-policy/';

    banner = document.createElement('div');
    banner.id = BANNER_ID;
    banner.className = 'insights-consent-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Cookie consent');
    banner.innerHTML =
      '<span class="insights-consent-text">' + text +
      (privacyUrl ? ' <a href="' + privacyUrl + '">Privacy</a>' : '') + '</span>' +
      '<span class="insights-consent-actions">' +
      '<button type="button" class="insights-consent-reject">Reject</button>' +
      '<button type="button" class="insights-consent-accept">Accept</button>' +
      '</span>';

    var acceptBtn = banner.querySelector('.insights-consent-accept');
    var rejectBtn = banner.querySelector('.insights-consent-reject');

    function close() {
      if (banner.parentNode) banner.parentNode.removeChild(banner);
    }

    acceptBtn.addEventListener('click', function () {
      setCookie(COOKIE_CONSENT, '1', 365);
      if (window.InsightsTracker && window.InsightsTracker.setConsent) {
        window.InsightsTracker.setConsent(true);
      }
      close();
    });

    rejectBtn.addEventListener('click', function () {
      setCookie(COOKIE_CONSENT, '0', 365);
      if (window.InsightsTracker && window.InsightsTracker.setConsent) {
        window.InsightsTracker.setConsent(false);
      }
      close();
    });

    document.body.appendChild(banner);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', showBannerIfNeeded);
  } else {
    showBannerIfNeeded();
  }
})();
