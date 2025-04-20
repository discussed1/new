/**
 * Discuss - Unified JavaScript functionality
 * Consolidated from multiple JS files to avoid redundancy and conflicts
 * Includes:
 * - Core application features
 * - AJAX voting system 
 * - Comment threading functionality
 * - Adaptive sizing system
 * - UI responsiveness
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded - initializing Discuss app features");
    
    // Set up comment replies
    setupCommentReplies();
    
    // Set up AJAX voting - load votes from localStorage first, then apply AJAX handlers
    loadVotesFromLocalStorage();
    setupAjaxVoting();
    
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0 && typeof bootstrap !== 'undefined') {
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => 
            new bootstrap.Tooltip(tooltipTriggerEl)
        );
    }
    
    // Initialize the adaptive sizing system
    initAdaptiveSystem();
    
    // Set initial adaptive scale based on screen size
    setAdaptiveScale();
    
    // Apply initial adaptive sizing to elements
    applyAdaptiveSizing();
    
    // Add responsive layout adjustments
    applyResponsiveLayout();
    
    // Add keyboard navigation support
    setupKeyboardNavigation();
    
    // Set active nav item based on current URL
    setActiveNavItem();
    
    // Initialize Reddit-style comment system if on a post detail page
    if (document.querySelector('.comment-thread')) {
        initRedditComments();
    }
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(alert => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';
            setTimeout(() => alert.style.display = 'none', 500);
        });
    }, 5000);
    
    // Handle window resize events for responsive adjustments and scaling
    window.addEventListener('resize', debounce(function() {
        // Update scale based on new viewport size
        setAdaptiveScale();
        // Apply updated adaptive sizing
        applyAdaptiveSizing();
        // Make responsive layout adjustments
        applyResponsiveLayout();
    }, 250));
});

/**
 * Applies specific layout adjustments based on screen size
 */
function applyResponsiveLayout() {
    const isMobile = window.innerWidth < 768;
    const isTablet = window.innerWidth >= 768 && window.innerWidth <= 1024;
    
    console.log(`Applying responsive layout: Mobile: ${isMobile}, Tablet: ${isTablet}`);
    
    // Apply mobile-specific layouts
    if (isMobile) {
        // Convert vote controls to horizontal on mobile
        document.querySelectorAll('.vote-controls').forEach(control => {
            control.classList.add('d-flex');
            control.classList.add('flex-row');
            control.classList.add('align-items-center');
            control.classList.remove('flex-column');
        });
        
        // Make sure tap targets are large enough (44px minimum)
        document.querySelectorAll('.btn, .nav-link, .vote-btn').forEach(elem => {
            elem.classList.add('mobile-friendly-tap');
        });
        
        // Stack flexbox elements that should be vertical on mobile
        document.querySelectorAll('.d-flex:not(.flex-column)').forEach(flex => {
            if (!flex.classList.contains('no-mobile-stack') && 
                !flex.classList.contains('navbar-nav') && 
                !flex.classList.contains('pagination')) {
                flex.classList.add('mobile-stack');
            }
        });
    } else {
        // Revert mobile changes for larger screens
        document.querySelectorAll('.vote-controls').forEach(control => {
            control.classList.remove('d-flex');
            control.classList.remove('flex-row');
            control.classList.remove('align-items-center');
            control.classList.add('flex-column');
        });
        
        document.querySelectorAll('.mobile-stack').forEach(elem => {
            elem.classList.remove('mobile-stack');
        });
    }
    
    // Apply tablet-specific layouts
    if (isTablet) {
        document.querySelectorAll('.sidebar').forEach(sidebar => {
            sidebar.classList.add('tablet-sidebar');
        });
    } else {
        document.querySelectorAll('.tablet-sidebar').forEach(sidebar => {
            sidebar.classList.remove('tablet-sidebar');
        });
    }
}

/**
 * Debounce function to limit how often a function is called
 */
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func.apply(context, args);
        }, wait);
    };
}

/**
 * Function to set active nav item based on current URL
 */
function setActiveNavItem() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || 
            (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        }
    });
}

/**
 * Format numbers for display (e.g., 1000 -> 1k)
 */
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'm';
    }
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'k';
    }
    return num;
}

/**
 * Function to create confirmation dialogs
 */
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

/**
 * Initialize the Reddit-style comment system
 */
function initRedditComments() {
    console.log("Initializing Reddit-style comments");
    
    // Set up collapsible threads
    setupThreadCollapsing();
    
    // Set up comment voting
    setupCommentVoting();
    
    // Initialize any collapsed threads from localStorage
    loadCollapsedThreads();
}

/**
 * Set up the collapsible thread functionality
 */
function setupThreadCollapsing() {
    // Get all thread collapse lines
    const collapseLines = document.querySelectorAll('.thread-collapse-line');
    const rootComments = document.querySelectorAll('.comment-thread > .comment-item .collapse-indicator');
    
    // Add event listeners to thread collapse lines
    collapseLines.forEach(line => {
        line.addEventListener('click', toggleThreadCollapse);
        line.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleThreadCollapse.call(this, e);
            }
        });
    });
    
    // Add event listeners to root comment collapse indicators
    rootComments.forEach(indicator => {
        indicator.parentElement.addEventListener('click', function(e) {
            // Only collapse if clicking on the meta area with the username/etc
            if (e.target.closest('.comment-body') || e.target.closest('.comment-actions') || e.target.closest('.reply-form')) {
                return;
            }
            
            // Get the thread-id from the parent comment-thread
            const threadItem = this.closest('.comment-thread');
            if (threadItem) {
                const threadId = threadItem.dataset.commentId;
                toggleThreadCollapseById(threadId);
            }
        });
    });
}

/**
 * Toggle thread collapse/expand
 */
function toggleThreadCollapse(e) {
    e.preventDefault();
    const threadId = this.dataset.threadId;
    toggleThreadCollapseById(threadId);
}

/**
 * Toggle thread collapse/expand by comment ID
 */
function toggleThreadCollapseById(threadId) {
    const thread = document.getElementById(`thread-${threadId}`);
    
    if (!thread) return;
    
    const isCollapsed = thread.classList.contains('collapsed');
    const nestedComments = thread.querySelector('.nested-comments');
    
    if (isCollapsed) {
        // Expand the thread
        thread.classList.remove('collapsed');
        if (nestedComments) {
            nestedComments.classList.add('animate-in');
            nestedComments.classList.remove('animate-out');
        }
        // Remove from localStorage
        removeCollapsedThread(threadId);
    } else {
        // Collapse the thread
        thread.classList.add('collapsed');
        if (nestedComments) {
            nestedComments.classList.remove('animate-in');
            nestedComments.classList.add('animate-out');
        }
        // Save to localStorage
        saveCollapsedThread(threadId);
    }
}

/**
 * Save collapsed thread state to localStorage
 */
function saveCollapsedThread(threadId) {
    // Get current collapsed threads
    let collapsedThreads = JSON.parse(localStorage.getItem('collapsedThreads') || '[]');
    
    // Add this thread if not already included
    if (!collapsedThreads.includes(threadId)) {
        collapsedThreads.push(threadId);
        localStorage.setItem('collapsedThreads', JSON.stringify(collapsedThreads));
    }
}

/**
 * Remove thread from collapsed state in localStorage
 */
function removeCollapsedThread(threadId) {
    // Get current collapsed threads
    let collapsedThreads = JSON.parse(localStorage.getItem('collapsedThreads') || '[]');
    
    // Remove this thread if included
    const index = collapsedThreads.indexOf(threadId);
    if (index !== -1) {
        collapsedThreads.splice(index, 1);
        localStorage.setItem('collapsedThreads', JSON.stringify(collapsedThreads));
    }
}

/**
 * Load collapsed threads from localStorage
 */
function loadCollapsedThreads() {
    // Get collapsed threads from localStorage
    const collapsedThreads = JSON.parse(localStorage.getItem('collapsedThreads') || '[]');
    
    // Collapse each thread
    collapsedThreads.forEach(threadId => {
        const thread = document.getElementById(`thread-${threadId}`);
        if (thread) {
            thread.classList.add('collapsed');
        }
    });
}

/**
 * Set up comment voting with AJAX
 */
function setupCommentVoting() {
    // This will use the global setupAjaxVoting function
    // We don't need a separate implementation
}

/**
 * Sets up keyboard navigation for interactive elements
 */
function setupKeyboardNavigation() {
    // Add keyboard support for vote buttons
    document.querySelectorAll('.vote-btn').forEach(btn => {
        btn.addEventListener('keydown', function(e) {
            if (e.key === ' ' || e.key === 'Enter') {
                e.preventDefault();
                this.click();
            }
        });
    });
    
    // Add keyboard support for any custom dropdown toggles
    document.querySelectorAll('[data-toggle]').forEach(toggle => {
        toggle.addEventListener('keydown', function(e) {
            if (e.key === ' ' || e.key === 'Enter') {
                e.preventDefault();
                this.click();
            }
        });
    });
}

function setupCommentReplies() {
    console.log("Setting up comment replies");
    
    // Get all reply toggle buttons
    const replyToggles = document.querySelectorAll('.reply-toggle');
    console.log("Found reply toggles:", replyToggles.length);
    
    // Add click event listener to each reply toggle
    replyToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const commentId = this.getAttribute('data-comment-id');
            const replyForm = document.getElementById(`reply-form-${commentId}`);
            
            console.log("Toggling reply form for comment ID:", commentId);
            console.log("Reply form element:", replyForm);
            
            // Hide all other reply forms first
            document.querySelectorAll('.reply-form').forEach(form => {
                if (form.id !== `reply-form-${commentId}`) {
                    form.style.display = 'none';
                    const toggleButton = document.querySelector(`.reply-toggle[data-comment-id="${form.id.replace('reply-form-', '')}"]`);
                    if (toggleButton) {
                        toggleButton.setAttribute('aria-expanded', 'false');
                    }
                    form.setAttribute('aria-hidden', 'true');
                }
            });
            
            // Toggle this reply form
            if (replyForm) {
                // Toggle visibility
                const isCurrentlyHidden = replyForm.style.display === 'none' || replyForm.style.display === '';
                replyForm.style.display = isCurrentlyHidden ? 'block' : 'none';
                
                // Update ARIA attributes
                this.setAttribute('aria-expanded', isCurrentlyHidden ? 'true' : 'false');
                replyForm.setAttribute('aria-hidden', isCurrentlyHidden ? 'false' : 'true');
                
                // Announce to screen readers
                if (window.announceToScreenReader) {
                    window.announceToScreenReader(isCurrentlyHidden ? 'Reply form opened' : 'Reply form closed');
                }
                
                // If showing the form, focus on the textarea
                if (isCurrentlyHidden) {
                    // Focus on the textarea
                    const textarea = replyForm.querySelector('textarea');
                    if (textarea) {
                        setTimeout(() => {
                            textarea.focus();
                        }, 50);
                    }
                }
            } else {
                console.error("Reply form not found for comment ID:", commentId);
            }
        });
    });
    
    // Get all cancel reply buttons
    const cancelButtons = document.querySelectorAll('.cancel-reply');
    console.log("Found cancel buttons:", cancelButtons.length);
    
    // Add click event to each cancel button
    cancelButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const commentId = this.getAttribute('data-comment-id');
            const replyForm = document.getElementById(`reply-form-${commentId}`);
            const replyToggle = document.querySelector(`.reply-toggle[data-comment-id="${commentId}"]`);
            
            if (replyForm) {
                replyForm.style.display = 'none';
                replyForm.setAttribute('aria-hidden', 'true');
                
                if (replyToggle) {
                    replyToggle.setAttribute('aria-expanded', 'false');
                    // Focus back to reply toggle when canceling
                    replyToggle.focus();
                }
                
                // Announce to screen readers
                if (window.announceToScreenReader) {
                    window.announceToScreenReader('Reply canceled');
                }
            }
        });
    });
}

/**
 * Initialize the adaptive sizing system
 */
function initAdaptiveSystem() {
    // Add our custom CSS variables for unified adaptive sizing
    const style = document.createElement('style');
    style.innerHTML = `
        :root {
            --adaptive-scale: 1;
            --mobile-scale: 0.85;
            --tablet-scale: 0.92;
            --desktop-scale: 1;
            --large-desktop-scale: 1.1;
            
            /* Spacing variables */
            --base-spacing: calc(0.5rem * var(--adaptive-scale));
            --spacing-xs: calc(0.25rem * var(--adaptive-scale));
            --spacing-sm: calc(0.5rem * var(--adaptive-scale));
            --spacing-md: calc(1rem * var(--adaptive-scale));
            --spacing-lg: calc(1.5rem * var(--adaptive-scale));
            --spacing-xl: calc(2rem * var(--adaptive-scale));
            
            /* Font size variables */
            --font-size-xs: calc(0.75rem * var(--adaptive-scale));
            --font-size-sm: calc(0.875rem * var(--adaptive-scale));
            --font-size-md: calc(1rem * var(--adaptive-scale));
            --font-size-lg: calc(1.25rem * var(--adaptive-scale));
            --font-size-xl: calc(1.5rem * var(--adaptive-scale));
            --font-size-xxl: calc(2rem * var(--adaptive-scale));
            
            /* Border radius */
            --border-radius-sm: calc(0.25rem * var(--adaptive-scale));
            --border-radius-md: calc(0.5rem * var(--adaptive-scale));
            --border-radius-lg: calc(0.75rem * var(--adaptive-scale));
            
            /* Icon sizes */
            --icon-size-sm: calc(1rem * var(--adaptive-scale));
            --icon-size-md: calc(1.5rem * var(--adaptive-scale));
            --icon-size-lg: calc(2rem * var(--adaptive-scale));
        }
    `;
    document.head.appendChild(style);
    
    // Set up adaptive scale based on screen size
    setAdaptiveScale();
    
    // Listen for window resize events to update adaptive scale
    window.addEventListener('resize', debounce(setAdaptiveScale, 100));
}

/**
 * Apply adaptive sizing to all elements
 */
function applyAdaptiveSizing() {
    // Apply font sizes
    document.querySelectorAll('.adaptive-text-xs').forEach(el => {
        el.style.fontSize = 'var(--font-size-xs)';
    });
    
    document.querySelectorAll('.adaptive-text-sm').forEach(el => {
        el.style.fontSize = 'var(--font-size-sm)';
    });
    
    document.querySelectorAll('.adaptive-text-md').forEach(el => {
        el.style.fontSize = 'var(--font-size-md)';
    });
    
    document.querySelectorAll('.adaptive-text-lg').forEach(el => {
        el.style.fontSize = 'var(--font-size-lg)';
    });
    
    document.querySelectorAll('.adaptive-text-xl').forEach(el => {
        el.style.fontSize = 'var(--font-size-xl)';
    });
    
    // Apply spacing
    document.querySelectorAll('.adaptive-p').forEach(el => {
        el.style.padding = 'var(--spacing-md)';
    });
    
    document.querySelectorAll('.adaptive-m').forEach(el => {
        el.style.margin = 'var(--spacing-md)';
    });
    
    document.querySelectorAll('.adaptive-gap').forEach(el => {
        el.style.gap = 'var(--spacing-md)';
    });
    
    // Apply adaptive sizing to specific components
    document.querySelectorAll('.vote-btn').forEach(btn => {
        btn.style.fontSize = 'var(--font-size-lg)';
    });
    
    document.querySelectorAll('.comment-meta').forEach(meta => {
        meta.style.fontSize = 'var(--font-size-xs)';
    });
    
    document.querySelectorAll('.post-title').forEach(title => {
        title.style.fontSize = 'var(--font-size-xl)';
    });
    
    document.querySelectorAll('.community-name').forEach(name => {
        name.style.fontSize = 'var(--font-size-md)';
    });
    
    // Apply adaptive spacing to specific components
    document.querySelectorAll('.post-card').forEach(card => {
        card.style.padding = 'var(--spacing-md)';
        card.style.margin = 'var(--spacing-md) 0';
        card.style.borderRadius = 'var(--border-radius-md)';
    });
    
    document.querySelectorAll('.comment-item').forEach(item => {
        item.style.marginBottom = 'var(--spacing-sm)';
        item.style.paddingLeft = 'var(--spacing-md)';
    });
    
    document.querySelectorAll('.thread-collapse-line').forEach(line => {
        line.style.width = 'var(--spacing-xs)';
    });
    
    // Apply adaptive icon sizes
    document.querySelectorAll('.icon-sm').forEach(icon => {
        icon.style.width = 'var(--icon-size-sm)';
        icon.style.height = 'var(--icon-size-sm)';
    });
    
    document.querySelectorAll('.icon-md').forEach(icon => {
        icon.style.width = 'var(--icon-size-md)';
        icon.style.height = 'var(--icon-size-md)';
    });
    
    document.querySelectorAll('.icon-lg').forEach(icon => {
        icon.style.width = 'var(--icon-size-lg)';
        icon.style.height = 'var(--icon-size-lg)';
    });
}

/**
 * Set the adaptive scale based on screen size
 * Uses a more nuanced approach with fluid scaling between breakpoints
 */
function setAdaptiveScale() {
    let adaptiveScale;
    const viewportWidth = window.innerWidth;
    
    // Base scale for different device sizes
    // These create a smooth transition between device sizes rather than jumps
    if (viewportWidth < 576) {
        // Mobile phones - smaller scale for better proportions
        adaptiveScale = 0.85;
    } else if (viewportWidth < 768) {
        // Large phones and small tablets - calculate fluid scale between 0.85 and 0.9
        const ratio = (viewportWidth - 576) / (768 - 576);
        adaptiveScale = 0.85 + (ratio * 0.05);
    } else if (viewportWidth < 992) {
        // Tablets - calculate fluid scale between 0.9 and 0.92
        const ratio = (viewportWidth - 768) / (992 - 768);
        adaptiveScale = 0.9 + (ratio * 0.02);
    } else if (viewportWidth < 1200) {
        // Smaller desktops - gradually increase to full scale
        const ratio = (viewportWidth - 992) / (1200 - 992);
        adaptiveScale = 0.92 + (ratio * 0.08);
    } else if (viewportWidth < 1600) {
        // Standard desktops - full scale
        adaptiveScale = 1;
    } else {
        // Large desktops - slightly larger, but not too much
        // Using Math.min to cap the scale for extremely large screens
        const maxScale = 1.05; // Reduced from 1.1 to keep proportions better balanced
        adaptiveScale = Math.min(1 + ((viewportWidth - 1600) / 2000) * 0.05, maxScale);
    }
    
    // Set the CSS variable
    document.documentElement.style.setProperty('--adaptive-scale', adaptiveScale);
    console.log("Setting adaptive scale to:", adaptiveScale);
}

function setupAjaxVoting() {
    console.log("Setting up AJAX voting");
    
    // Load existing votes from localStorage first
    loadVotesFromLocalStorage();
    
    // For post votes
    const postVoteButtons = document.querySelectorAll('.post-vote-btn');
    console.log("Found post vote buttons:", postVoteButtons.length);
    
    postVoteButtons.forEach(button => {
        // Make sure buttons are focusable and handle keyboard events
        button.setAttribute('role', 'button');
        button.setAttribute('tabindex', '0');
        
        // Add keyboard event listeners
        button.addEventListener('keydown', function(e) {
            if (e.key === ' ' || e.key === 'Enter') {
                e.preventDefault();
                this.click();
            }
        });
        
        button.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("Post vote button clicked:", this.href);
            
            // Only process authenticated user clicks
            if (this.href.includes('login')) {
                window.location.href = this.href;
                return;
            }
            
            // Show loading state
            this.setAttribute('aria-busy', 'true');
            
            const voteUrl = this.href;
            const isUpvote = voteUrl.includes('upvote');
            const voteType = isUpvote ? 'upvote' : 'downvote';
            
            // Get CSRF token
            const csrfToken = getCsrfToken();
            console.log("Using CSRF token for post vote:", csrfToken ? "Found token" : "No token found");
            
            // Logging details for debugging
            console.log("Sending post vote request to:", voteUrl);
            
            // For GET requests, we don't technically need to set CSRF
            // But we'll prepare headers properly for future compatibility
            const headers = {
                'X-Requested-With': 'XMLHttpRequest'
            };
            
            // Only add CSRF token for non-GET requests, but we'll set it anyway
            if (csrfToken) {
                headers['X-CSRFToken'] = csrfToken;
                console.log("Added CSRF token to post vote request headers");
            }
            
            fetch(voteUrl, {
                method: 'GET',  // Django view is only set up for GET requests currently
                headers: headers,
                credentials: 'include' // Include cookies in the request (include works across domains)
            })
            .then(response => response.json())
            .then(data => {
                console.log("Vote response data:", data);
                
                // Update the vote count display
                const postId = data.post_id;
                const voteCountElement = document.getElementById(`post-${postId}-votes`);
                if (voteCountElement) {
                    voteCountElement.textContent = data.vote_count;
                    console.log(`Updated vote count to ${data.vote_count}`);
                    
                    // Update ARIA attributes for screen readers
                    voteCountElement.setAttribute('aria-label', `Post score: ${data.vote_count}`);
                    
                    // Announce the vote to screen readers
                    if (window.announceToScreenReader) {
                        window.announceToScreenReader(`Post ${voteType}d. Score is now ${data.vote_count}`);
                    }
                } else {
                    console.error(`Vote count element not found for post-${postId}-votes`);
                }
                
                // Update active state of vote buttons for this post
                const upvoteBtn = document.querySelector(`.post-vote-btn[href*="/posts/${postId}/vote/upvote"]`);
                const downvoteBtn = document.querySelector(`.post-vote-btn[href*="/posts/${postId}/vote/downvote"]`);
                
                console.log("Found upvote button:", upvoteBtn ? "yes" : "no");
                console.log("Found downvote button:", downvoteBtn ? "yes" : "no");
                console.log("Current user vote value:", data.user_vote);
                
                if (upvoteBtn) {
                    if (data.user_vote === 1) {
                        upvoteBtn.classList.add('voted');
                        upvoteBtn.classList.add('active');
                        upvoteBtn.setAttribute('aria-pressed', 'true');
                        console.log("Added 'voted' and 'active' classes to upvote button");
                    } else {
                        upvoteBtn.classList.remove('voted');
                        upvoteBtn.classList.remove('active');
                        upvoteBtn.setAttribute('aria-pressed', 'false');
                        console.log("Removed 'voted' and 'active' classes from upvote button");
                    }
                }
                
                if (downvoteBtn) {
                    if (data.user_vote === -1) {
                        downvoteBtn.classList.add('voted');
                        downvoteBtn.classList.add('active');
                        downvoteBtn.setAttribute('aria-pressed', 'true');
                        console.log("Added 'voted' and 'active' classes to downvote button");
                    } else {
                        downvoteBtn.classList.remove('voted');
                        downvoteBtn.classList.remove('active');
                        downvoteBtn.setAttribute('aria-pressed', 'false');
                        console.log("Removed 'voted' and 'active' classes from downvote button");
                    }
                }
                
                // Save the vote state to localStorage
                saveVoteToLocalStorage('post', postId, data.user_vote);
            })
            .catch(error => {
                console.error('Error:', error);
                if (window.announceToScreenReader) {
                    window.announceToScreenReader('Error processing vote');
                }
            })
            .finally(() => {
                // Remove loading state
                this.setAttribute('aria-busy', 'false');
            });
        });
    });
    
    // For comment votes
    const commentVoteButtons = document.querySelectorAll('.comment-vote-btn');
    console.log("Found comment vote buttons:", commentVoteButtons.length);
    
    commentVoteButtons.forEach(button => {
        // Make sure buttons are focusable and handle keyboard events
        button.setAttribute('role', 'button');
        button.setAttribute('tabindex', '0');
        
        // Add keyboard event listeners
        button.addEventListener('keydown', function(e) {
            if (e.key === ' ' || e.key === 'Enter') {
                e.preventDefault();
                this.click();
            }
        });
        
        button.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("Comment vote button clicked:", this.href);
            
            // Only process authenticated user clicks
            if (this.href.includes('login')) {
                window.location.href = this.href;
                return;
            }
            
            // Show loading state
            this.setAttribute('aria-busy', 'true');
            
            const voteUrl = this.href;
            const isUpvote = voteUrl.includes('upvote');
            const voteType = isUpvote ? 'upvote' : 'downvote';
            
            // Get CSRF token
            const csrfToken = getCsrfToken();
            console.log("Using CSRF token for comment vote:", csrfToken ? "Found token" : "No token found");
            
            // Logging details for debugging
            console.log("Sending comment vote request to:", voteUrl);
            
            // For GET requests, we don't technically need to set CSRF
            // But we'll prepare headers properly for future compatibility
            const headers = {
                'X-Requested-With': 'XMLHttpRequest'
            };
            
            // Only add CSRF token for non-GET requests, but we'll set it anyway
            if (csrfToken) {
                headers['X-CSRFToken'] = csrfToken;
                console.log("Added CSRF token to comment vote request headers");
            }
            
            fetch(voteUrl, {
                method: 'GET',  // Django view is only set up for GET requests currently
                headers: headers,
                credentials: 'include' // Include cookies in the request (include works across domains)
            })
            .then(response => response.json())
            .then(data => {
                console.log("Comment vote response data:", data);
                
                // Update the vote count display
                const commentId = data.comment_id;
                const commentElement = document.getElementById(`comment-${commentId}`);
                if (commentElement) {
                    const voteCountElement = commentElement.querySelector('.vote-count');
                    if (voteCountElement) {
                        voteCountElement.textContent = data.vote_count;
                        console.log(`Updated comment vote count to ${data.vote_count}`);
                        
                        // Update ARIA attributes for screen readers
                        voteCountElement.setAttribute('aria-label', `Comment score: ${data.vote_count}`);
                        
                        // Announce the vote to screen readers
                        if (window.announceToScreenReader) {
                            window.announceToScreenReader(`Comment ${voteType}d. Score is now ${data.vote_count}`);
                        }
                    } else {
                        console.error(`Vote count element not found for comment ${commentId}`);
                    }
                    
                    // Update vote button styles
                    const upvoteBtn = commentElement.querySelector('a[href*="upvote"]');
                    const downvoteBtn = commentElement.querySelector('a[href*="downvote"]');
                    
                    console.log("Found comment upvote button:", upvoteBtn ? "yes" : "no");
                    console.log("Found comment downvote button:", downvoteBtn ? "yes" : "no");
                    console.log("Current user comment vote value:", data.user_vote);
                    
                    if (upvoteBtn) {
                        if (data.user_vote === 1) {
                            upvoteBtn.classList.add('voted');
                            upvoteBtn.classList.add('active');
                            upvoteBtn.setAttribute('aria-pressed', 'true');
                            console.log("Added 'voted' and 'active' classes to comment upvote button");
                        } else {
                            upvoteBtn.classList.remove('voted');
                            upvoteBtn.classList.remove('active');
                            upvoteBtn.setAttribute('aria-pressed', 'false');
                            console.log("Removed 'voted' and 'active' classes from comment upvote button");
                        }
                    }
                    
                    if (downvoteBtn) {
                        if (data.user_vote === -1) {
                            downvoteBtn.classList.add('voted');
                            downvoteBtn.classList.add('active');
                            downvoteBtn.setAttribute('aria-pressed', 'true');
                            console.log("Added 'voted' and 'active' classes to comment downvote button");
                        } else {
                            downvoteBtn.classList.remove('voted');
                            downvoteBtn.classList.remove('active');
                            downvoteBtn.setAttribute('aria-pressed', 'false');
                            console.log("Removed 'voted' and 'active' classes from comment downvote button");
                        }
                    }
                    
                    // Save the vote state to localStorage
                    saveVoteToLocalStorage('comment', commentId, data.user_vote);
                } else {
                    console.error(`Comment element not found for comment-${commentId}`);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (window.announceToScreenReader) {
                    window.announceToScreenReader('Error processing vote');
                }
            })
            .finally(() => {
                // Remove loading state
                this.setAttribute('aria-busy', 'false');
            });
        });
    });
}

// Function to get CSRF token
function getCsrfToken() {
    // First try to get it from the meta tag (Django sets this with {% csrf_token %})
    const metaToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    if (metaToken) {
        console.log("Found CSRF token in meta tag");
        return metaToken;
    }
    
    // Then try to get it from the cookie (Django's default method)
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    
    if (cookieValue) {
        console.log("Found CSRF token in cookie");
        return cookieValue;
    }
    
    // Finally try to get it from a form input
    const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (csrfInput) {
        console.log("Found CSRF token in form input");
        return csrfInput.value;
    }
    
    console.error('CSRF token not found!');
    return '';
}

// Save vote to localStorage - this is similar to how Reddit persists vote state
function saveVoteToLocalStorage(type, id, value) {
    try {
        if (type && id) {
            const key = `discuss_${type}_vote_${id}`;
            console.log(`Saving vote to localStorage: ${key} = ${value}`);
            localStorage.setItem(key, value);
        }
    } catch (e) {
        console.error('Error saving vote to localStorage:', e);
    }
}

// Load votes from localStorage and apply them
function loadVotesFromLocalStorage() {
    try {
        console.log("Loading votes from localStorage");
        
        // For posts
        document.querySelectorAll('.post-vote-btn').forEach(btn => {
            const href = btn.getAttribute('href');
            if (!href) return;
            
            const postIdMatch = href.match(/posts\/(\d+)\/vote\/(up|down)vote/);
            
            if (postIdMatch && postIdMatch[1]) {
                const postId = postIdMatch[1];
                const voteType = postIdMatch[2]; // 'up' or 'down'
                const key = `discuss_post_vote_${postId}`;
                const savedVote = localStorage.getItem(key);
                
                console.log(`Checking saved vote for post ${postId}: ${savedVote}`);
                
                if (savedVote === '1' && voteType === 'up') {
                    btn.classList.add('voted');
                    btn.classList.add('active');
                    console.log(`Applied saved upvote for post ${postId}`);
                } else if (savedVote === '-1' && voteType === 'down') {
                    btn.classList.add('voted');
                    btn.classList.add('active');
                    console.log(`Applied saved downvote for post ${postId}`);
                }
            }
        });
        
        // For comments
        document.querySelectorAll('.comment-vote-btn').forEach(btn => {
            const href = btn.getAttribute('href');
            if (!href) return;
            
            const commentIdMatch = href.match(/comments\/(\d+)\/vote\/(up|down)vote/);
            
            if (commentIdMatch && commentIdMatch[1]) {
                const commentId = commentIdMatch[1];
                const voteType = commentIdMatch[2]; // 'up' or 'down'
                const key = `discuss_comment_vote_${commentId}`;
                const savedVote = localStorage.getItem(key);
                
                console.log(`Checking saved vote for comment ${commentId}: ${savedVote}`);
                
                if (savedVote === '1' && voteType === 'up') {
                    btn.classList.add('voted');
                    btn.classList.add('active');
                    console.log(`Applied saved upvote for comment ${commentId}`);
                } else if (savedVote === '-1' && voteType === 'down') {
                    btn.classList.add('voted');
                    btn.classList.add('active');
                    console.log(`Applied saved downvote for comment ${commentId}`);
                }
            }
        });
    } catch (e) {
        console.error('Error loading votes from localStorage:', e);
    }
}

/**
 * Donation Form Toggle Functionality
 * Controls the visibility of the custom amount input field based on donation type selection
 */
function toggleCustomAmount() {
    const donationTypeSelect = document.getElementById('id_donation_type');
    const customAmountGroup = document.getElementById('custom-amount-group');
    
    if (!donationTypeSelect || !customAmountGroup) {
        return; // Exit if we're not on the donation page
    }
    
    if (donationTypeSelect.value === '0') {
        customAmountGroup.style.display = 'block';
    } else {
        customAmountGroup.style.display = 'none';
    }
}

// Initialize donation form functionality if on donation page
document.addEventListener('DOMContentLoaded', function() {
    const donationTypeSelect = document.getElementById('id_donation_type');
    
    if (donationTypeSelect) {
        console.log("Initializing donation form");
        toggleCustomAmount();
        
        // Add event listener for when the donation type changes
        donationTypeSelect.addEventListener('change', toggleCustomAmount);
    }
    
    // Initialize payment method visibility on the payment/confirmation page
    initPaymentMethodVisibility();
});

/**
 * Initialize and handle payment method visibility on the payment/confirmation page
 */
function initPaymentMethodVisibility() {
    // Check if we're on a page with payment method options
    const paymentRadios = document.querySelectorAll('.payment-method-radio');
    
    if (paymentRadios.length) {
        console.log("Initializing payment method visibility");
        
        // Hide all payment details initially
        updatePaymentMethodVisibility();
        
        // Add change event listeners to radio buttons
        paymentRadios.forEach(radio => {
            radio.addEventListener('change', updatePaymentMethodVisibility);
        });
    }
}

/**
 * Show only the selected payment method details and hide others
 */
function updatePaymentMethodVisibility() {
    const paymentDetails = document.querySelectorAll('.payment-method-details');
    const selectedMethod = document.querySelector('.payment-method-radio:checked');
    
    // Hide all details sections
    paymentDetails.forEach(detail => {
        detail.style.display = 'none';
    });
    
    // Show only the selected method's details
    if (selectedMethod) {
        const detailsId = selectedMethod.value + '-details';
        const detailsElement = document.getElementById(detailsId);
        if (detailsElement) {
            detailsElement.style.display = 'block';
        }
    }
}

/**
 * Accessibility Enhancements
 * Improves application accessibility for screen readers and keyboard navigation
 */
function setupAccessibility() {
    // Fix any missing aria attributes dynamically
    const buttons = document.querySelectorAll('button:not([aria-label])');
    buttons.forEach(button => {
        const buttonText = button.textContent.trim();
        if (buttonText) {
            button.setAttribute('aria-label', buttonText);
        }
    });
    
    // Add keyboard support for custom components
    const voteButtons = document.querySelectorAll('.vote-btn');
    voteButtons.forEach(button => {
        button.addEventListener('keydown', function(e) {
            if (e.code === 'Space' || e.code === 'Enter') {
                e.preventDefault();
                button.click();
            }
        });
    });
    
    // Make dynamic content announcements for screen readers
    const announcementDiv = document.createElement('div');
    announcementDiv.setAttribute('aria-live', 'polite');
    announcementDiv.classList.add('sr-only');
    document.body.appendChild(announcementDiv);
    
    window.announceToScreenReader = function(message) {
        announcementDiv.textContent = message;
        setTimeout(() => { announcementDiv.textContent = ''; }, 3000);
    };
}

// Initialize accessibility enhancements
document.addEventListener('DOMContentLoaded', setupAccessibility);
