import re, os

# The files to update
files = [
    "index.html",
    "home2.html",
    "about.html",
    "booking.html",
    "contact.html",
    "gallery.html",
    "services.html",
    "servicedetails.html",
]

# The desktop toggle HTML to inject (replaces the old two-button div)
DESKTOP_TOGGLE = '''<div class="auth-toggle-wrap flex-shrink-0 ml-3" role="tablist" aria-label="Authentication options">
                        <div class="auth-toggle-pill" id="auth-toggle">
                            <!-- Sliding indicator -->
                            <span class="auth-toggle-indicator" id="auth-toggle-indicator" aria-hidden="true"></span>
                            <!-- Login tab -->
                            <a href="login.html"
                               role="tab"
                               id="auth-tab-login"
                               class="auth-toggle-tab auth-toggle-tab--active"
                               aria-selected="true">
                               Login
                            </a>
                            <!-- Sign Up tab -->
                            <a href="signup.html"
                               role="tab"
                               id="auth-tab-signup"
                               class="auth-toggle-tab"
                               aria-selected="false">
                               Sign Up
                            </a>
                        </div>
                    </div>'''

# CSS to insert into each <style> block (before </style>)
TOGGLE_CSS = """
        /* ===== AUTH TOGGLE SWITCH (Desktop Only) ===== */
        .auth-toggle-wrap {
            display: none; /* hidden on mobile by default */
        }
        @media (min-width: 1280px) { /* xl breakpoint = Tailwind xl */
            .auth-toggle-wrap { display: flex; align-items: center; }
        }
        .auth-toggle-pill {
            position: relative;
            display: inline-flex;
            align-items: center;
            background-color: var(--color-hover);
            border: 1px solid var(--color-border);
            border-radius: 9999px;
            padding: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            gap: 0;
            overflow: hidden;
        }
        html[data-theme='dark'] .auth-toggle-pill {
            background-color: #1B2E23;
            border-color: #2D5A3F;
            box-shadow: 0 2px 12px rgba(0,0,0,0.3);
        }
        .auth-toggle-indicator {
            position: absolute;
            top: 4px;
            bottom: 4px;
            left: 4px;
            width: calc(50% - 4px);
            background-color: var(--color-accent);
            border-radius: 9999px;
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                        width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 0;
            box-shadow: 0 2px 8px rgba(31,61,43,0.25);
        }
        html[data-theme='dark'] .auth-toggle-indicator {
            background-color: var(--color-accent-light);
            box-shadow: 0 2px 8px rgba(230,179,37,0.3);
        }
        /* Slide indicator to right when signup is active */
        .auth-toggle-pill[data-active="signup"] .auth-toggle-indicator {
            transform: translateX(calc(100% + 0px));
        }
        .auth-toggle-tab {
            position: relative;
            z-index: 1;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.45rem 1.2rem;
            border-radius: 9999px;
            font-weight: 700;
            font-size: 0.875rem;
            letter-spacing: 0.01em;
            color: var(--color-secondary-text);
            text-decoration: none;
            transition: color 0.25s ease;
            white-space: nowrap;
            user-select: none;
            -webkit-user-select: none;
            min-width: 72px;
            text-align: center;
        }
        .auth-toggle-tab--active {
            color: #ffffff;
        }
        html[data-theme='dark'] .auth-toggle-tab--active {
            color: #000000;
        }
        .auth-toggle-tab:not(.auth-toggle-tab--active):hover {
            color: var(--color-accent);
        }
        html[data-theme='dark'] .auth-toggle-tab:not(.auth-toggle-tab--active):hover {
            color: var(--color-accent-light);
        }
        /* Keyboard focus ring */
        .auth-toggle-tab:focus-visible {
            outline: 2px solid var(--color-accent-light);
            outline-offset: 2px;
            border-radius: 9999px;
        }
"""

# JS to inject before </script> close in each file (or before </body>)
TOGGLE_JS = """
    // ===== AUTH TOGGLE LOGIC =====
    (function() {
        var pill = document.getElementById('auth-toggle');
        if (!pill) return;
        var loginTab = document.getElementById('auth-tab-login');
        var signupTab = document.getElementById('auth-tab-signup');
        var indicator = document.getElementById('auth-toggle-indicator');
        var page = window.location.pathname.split('/').pop() || '';

        function setActive(tab) {
            if (tab === 'signup') {
                pill.setAttribute('data-active', 'signup');
                loginTab.classList.remove('auth-toggle-tab--active');
                loginTab.setAttribute('aria-selected', 'false');
                signupTab.classList.add('auth-toggle-tab--active');
                signupTab.setAttribute('aria-selected', 'true');
            } else {
                pill.setAttribute('data-active', 'login');
                signupTab.classList.remove('auth-toggle-tab--active');
                signupTab.setAttribute('aria-selected', 'false');
                loginTab.classList.add('auth-toggle-tab--active');
                loginTab.setAttribute('aria-selected', 'true');
            }
        }

        // Highlight based on current page
        if (page === 'signup.html') { setActive('signup'); }
        else { setActive('login'); }

        // Keyboard: Enter/Space navigates
        [loginTab, signupTab].forEach(function(tab) {
            tab.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    window.location.href = tab.getAttribute('href');
                }
                if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
                    e.preventDefault();
                    var other = (tab === loginTab) ? signupTab : loginTab;
                    other.focus();
                }
            });
        });
    })();
"""

BASE = os.path.dirname(os.path.abspath(__file__))

# Pattern for the OLD desktop button block
# Handles both single-line and multi-line variants
OLD_DESKTOP_PATTERN = re.compile(
    r'<div\s+class="flex items-center gap-3 ml-3 flex-shrink-0">\s*'
    r'<a\s+href="login\.html"[^>]*>Login</a>\s*'
    r'<a\s+href="signup\.html"[^>]*>Sign[\s\S]*?Up</a>\s*'
    r'</div>',
    re.DOTALL
)

ok = []
skipped = []
for fname in files:
    path = os.path.join(BASE, fname)
    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()

    changed = False

    # 1) Replace desktop buttons
    if OLD_DESKTOP_PATTERN.search(src):
        src = OLD_DESKTOP_PATTERN.sub(DESKTOP_TOGGLE, src, count=1)
        changed = True
        print(f"[OK] {fname}: desktop buttons replaced")
    else:
        print(f"[WARN] {fname}: desktop pattern NOT found")

    # 2) Inject CSS into <style> block (before first </style>)
    if '/* ===== AUTH TOGGLE SWITCH' not in src:
        src = src.replace('</style>', TOGGLE_CSS + '\n    </style>', 1)
        changed = True
        print(f"[OK] {fname}: CSS injected")
    else:
        print(f"[SKIP] {fname}: CSS already present")

    # 3) Inject JS before </body>
    if '// ===== AUTH TOGGLE LOGIC' not in src:
        src = src.replace('</body>', TOGGLE_JS + '\n</body>', 1)
        changed = True
        print(f"[OK] {fname}: JS injected")
    else:
        print(f"[SKIP] {fname}: JS already present")

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(src)
        ok.append(fname)
    else:
        skipped.append(fname)

print("\n=== DONE ===")
print(f"Updated: {ok}")
print(f"Skipped: {skipped}")
