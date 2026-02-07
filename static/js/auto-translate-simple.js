/**
 * Simple Auto Translate System - No Loops
 * Lightweight version that doesn't cause infinite loops
 */

(function() {
    'use strict';

    let googleTranslateReady = false;
    let initialized = false;

    // Simple initialization - only once
    function initAutoTranslate() {
        if (initialized) return;
        
        // Check if Google Translate is loaded
        if (typeof google !== 'undefined' && google.translate && google.translate.TranslateElement) {
            googleTranslateReady = true;
            initialized = true;
            setupAutoTranslate();
            hideGoogleUI();
        }
    }

    // Aggressive hide function - completely remove Google Translate UI
    function hideGoogleUI() {
        try {
            // Remove banner completely - multiple selectors
            var banner = document.querySelector('.goog-te-banner-frame');
            if (banner) {
                banner.remove();
            }
            
            banner = document.querySelector('.goog-te-banner');
            if (banner) {
                banner.remove();
            }
            
            // Remove all Google Translate elements
            var allGoogle = document.querySelectorAll('.goog-te-banner, .goog-te-banner-frame, .goog-te-menu-frame, .goog-te-ftab, .goog-te-gadget, .goog-te-gadget-simple, .goog-te-menu-value');
            for (var i = 0; i < allGoogle.length; i++) {
                try {
                    allGoogle[i].remove();
                } catch (e) {}
            }
            
            // Remove iframes
            var iframes = document.querySelectorAll('iframe');
            for (var i = 0; i < iframes.length; i++) {
                try {
                    var src = iframes[i].src || '';
                    if (src.includes('translate.google.com') || src.includes('translate.googleapis.com')) {
                        iframes[i].remove();
                    }
                } catch (e) {}
            }
            
            // Reset body and html
            if (document.body) {
                document.body.style.top = '0';
                document.body.style.position = 'static';
                document.body.style.marginTop = '0';
                document.body.style.paddingTop = '0';
            }
            
            if (document.documentElement) {
                document.documentElement.style.marginTop = '0';
                document.documentElement.style.paddingTop = '0';
            }
            
            // Hide translate element but keep it functional
            var translateEl = document.getElementById('google_translate_element');
            if (translateEl) {
                translateEl.style.cssText = 'display: none !important; visibility: hidden !important; position: absolute !important; left: -9999px !important; top: -9999px !important; width: 0 !important; height: 0 !important; overflow: hidden !important; opacity: 0 !important; pointer-events: none !important; z-index: -9999 !important;';
            }
        } catch (e) {
            // Ignore errors
        }
    }
    
    // Watch for new Google Translate elements and remove them immediately
    function watchForGoogleElements() {
        var observer = new MutationObserver(function(mutations) {
            var removed = false;
            
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        // Check if it's a Google Translate element
                        if (node.classList) {
                            if (node.classList.contains('goog-te-banner') ||
                                node.classList.contains('goog-te-banner-frame') ||
                                node.classList.contains('goog-te-menu-frame') ||
                                node.classList.contains('goog-te-gadget') ||
                                node.classList.contains('goog-te-ftab')) {
                                try {
                                    node.remove();
                                    removed = true;
                                } catch (e) {}
                            }
                        }
                        
                        // Check iframe
                        if (node.tagName === 'IFRAME') {
                            try {
                                var src = node.src || '';
                                if (src.includes('translate.google.com') || src.includes('translate.googleapis.com')) {
                                    node.remove();
                                    removed = true;
                                }
                            } catch (e) {}
                        }
                        
                        // Also check children
                        if (node.querySelectorAll) {
                            var googleChildren = node.querySelectorAll('.goog-te-banner, .goog-te-banner-frame, .goog-te-menu-frame, iframe[src*="translate"]');
                            for (var i = 0; i < googleChildren.length; i++) {
                                try {
                                    googleChildren[i].remove();
                                    removed = true;
                                } catch (e) {}
                            }
                        }
                    }
                });
            });
            
            // Also hide any existing elements if something was removed
            if (removed) {
                hideGoogleUI();
            }
        });
        
        if (document.body) {
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        }
        
        // Also observe head for script tags
        if (document.head) {
            observer.observe(document.head, {
                childList: true,
                subtree: true
            });
        }
    }

    function setupAutoTranslate() {
        const currentLang = document.documentElement.lang || 'tr';
        const langMap = { 'tr': 'tr', 'en': 'en', 'fa': 'fa', 'ar': 'ar' };

        // Set cookie for initial language
        if (langMap[currentLang]) {
            try {
                document.cookie = `googtrans=/auto/${langMap[currentLang]}; path=/; max-age=31536000`;
            } catch (e) {}
        }

        // Set initial language after delay
        setTimeout(() => {
            if (langMap[currentLang]) {
                setLanguage(langMap[currentLang]);
            }
        }, 1500);

        // Hide UI
        hideGoogleUI();
    }

    // Global function to activate translation
    window.activateGoogleTranslate = function(langCode) {
        try {
            // Update button immediately
            document.querySelectorAll('.lang-btn').forEach(function(btn) {
                btn.classList.remove('active');
                if (btn.getAttribute('data-lang') === langCode) {
                    btn.classList.add('active');
                }
            });

            // Set cookie immediately
            try {
                document.cookie = `googtrans=/auto/${langCode}; path=/; max-age=31536000`;
            } catch (e) {}

            // Hide UI first
            hideGoogleUI();

            // Translate - try multiple times
            setLanguage(langCode);
            
            // Also try after a delay
            setTimeout(function() {
                setLanguage(langCode);
                hideGoogleUI();
            }, 500);
            
            setTimeout(function() {
                setLanguage(langCode);
                hideGoogleUI();
            }, 1000);
            
        } catch (e) {
            // Ignore errors
        }
    };

    function setLanguage(langCode) {
        // Set cookie first
        try {
            document.cookie = `googtrans=/auto/${langCode}; path=/; max-age=31536000`;
        } catch (e) {}
        
        // Find select element - try multiple times
        let select = null;
        let attempts = 0;
        const maxAttempts = 10;
        
        function findAndSetSelect() {
            select = document.querySelector('#google_translate_element select');
            if (!select) {
                select = document.querySelector('select.goog-te-combo');
            }
            if (!select) {
                const translateEl = document.getElementById('google_translate_element');
                if (translateEl) {
                    select = translateEl.querySelector('select');
                }
            }

            if (select) {
                const options = select.options;
                for (let i = 0; i < options.length; i++) {
                    const val = options[i].value;
                    if (val === langCode || 
                        val.startsWith(langCode + '|') || 
                        val.includes('|' + langCode) ||
                        (val.length === 2 && val === langCode)) {
                        select.selectedIndex = i;
                        
                        // Trigger multiple events
                        select.dispatchEvent(new Event('change', { bubbles: true, cancelable: true }));
                        select.dispatchEvent(new Event('input', { bubbles: true, cancelable: true }));
                        
                        try {
                            select.value = val;
                            select.dispatchEvent(new Event('change', { bubbles: true, cancelable: true }));
                        } catch (e) {}
                        
                        hideGoogleUI();
                        return true;
                    }
                }
            }
            
            return false;
        }
        
        // Try immediately
        if (!findAndSetSelect()) {
            // If not found, try again after delays
            attempts++;
            if (attempts < maxAttempts) {
                setTimeout(function() {
                    if (!findAndSetSelect()) {
                        setLanguage(langCode); // Retry
                    }
                }, 300);
            }
        }
        
        hideGoogleUI();
    }

    // Initialize
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initAutoTranslate();
            watchForGoogleElements();
            hideGoogleUI();
        });
    } else {
        initAutoTranslate();
        watchForGoogleElements();
        hideGoogleUI();
    }

    // Try once more after delay
    setTimeout(function() {
        initAutoTranslate();
        hideGoogleUI();
    }, 2000);
    
    // Hide UI periodically but with limit (to catch any new elements)
    let hideCount = 0;
    const hideInterval = setInterval(function() {
        if (hideCount++ < 30) { // 30 times = 60 seconds
            hideGoogleUI();
        } else {
            clearInterval(hideInterval);
        }
    }, 2000);
    
    // Start watching immediately
    watchForGoogleElements();
})();
