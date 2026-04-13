// Initialize Lucide icons
lucide.createIcons();
        
        // Re-initialize icons after a short delay to ensure they load
        setTimeout(() => {
            lucide.createIcons();
            console.log('Icons initialized');
        }, 100);

        // --- Enhanced Scroll Progress Bar ---
        const scrollProgress = document.querySelector('.scroll-progress');
        const scrollToTopBtn = document.getElementById('scroll-to-top');
        
        window.addEventListener('scroll', () => {
            const scrollTop = window.pageYOffset;
            const docHeight = document.body.offsetHeight - window.innerHeight;
            const scrollPercent = (scrollTop / docHeight) * 100;
            scrollProgress.style.width = scrollPercent + '%';
            
            // Show/hide scroll to top button
            if (scrollTop > 300) {
                scrollToTopBtn.style.opacity = '1';
                scrollToTopBtn.style.pointerEvents = 'auto';
            } else {
                scrollToTopBtn.style.opacity = '0';
                scrollToTopBtn.style.pointerEvents = 'none';
            }
        });
        
        // Scroll to top button functionality
        scrollToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
        
        // -- script for handling pop up msgs of forms ----
                document.getElementById("contact-form").addEventListener("submit", async function(e) {
            e.preventDefault();

            const form = e.target;
            const statusBox = document.getElementById("form-status");
            const formData = new FormData(form);

            try {
                const response = await fetch(form.action, {
                    method: form.method,
                    body: formData
                });

                const result = await response.json();

                if (result.success) {
                    statusBox.textContent = "✅ Message sent successfully!";
                    statusBox.className = "mt-6 p-4 rounded-lg text-center font-semibold bg-green-600 text-white";
                    form.reset();
                } else {
                    statusBox.textContent = "❌ Failed to send message. Try again!";
                    statusBox.className = "mt-6 p-4 rounded-lg text-center font-semibold bg-red-600 text-white";
                }
            } catch (error) {
                statusBox.textContent = "⚠️ Network error. Please try again later.";
                statusBox.className = "mt-6 p-4 rounded-lg text-center font-semibold bg-yellow-600 text-white";
            }

            statusBox.classList.remove("hidden");

            // ✅ Auto-hide after 5 seconds
            setTimeout(() => {
                statusBox.classList.add("hidden");
            }, 5000);
        });


        // --- Enhanced Active nav link highlighting with smooth transitions ---
        const sections = document.querySelectorAll('section');
        const mainNavListItems = document.querySelectorAll('#main-nav li, .mobile-menu-overlay li');
        const navIndicator = document.getElementById('nav-indicator');
        
        // Navigation click handlers - only scroll, no active state manipulation
        mainNavListItems.forEach(li => {
            const link = li.querySelector('a');
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href');
                const targetSection = document.querySelector(targetId);
                
                if (targetSection) {
                    // Remove any existing active classes immediately
                    mainNavListItems.forEach(item => item.classList.remove('active'));
                    
                    // Smooth scroll to target
                    targetSection.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
        
        // Mobile menu functionality
        const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
        const mobileMenuDropdown = document.getElementById('mobile-menu-dropdown');
        const hamburgerSpans = mobileMenuToggle.querySelectorAll('span');
        
        mobileMenuToggle.addEventListener('click', () => {
            // Toggle dropdown visibility
            mobileMenuDropdown.classList.toggle('opacity-0');
            mobileMenuDropdown.classList.toggle('invisible');
            mobileMenuDropdown.classList.toggle('-translate-y-2');
            mobileMenuDropdown.classList.toggle('opacity-100');
            mobileMenuDropdown.classList.toggle('visible');
            mobileMenuDropdown.classList.toggle('translate-y-0');
            
            // Animate hamburger to X
            hamburgerSpans[0].classList.toggle('rotate-45');
            hamburgerSpans[0].classList.toggle('translate-y-1.5');
            hamburgerSpans[1].classList.toggle('opacity-0');
            hamburgerSpans[2].classList.toggle('-rotate-45');
            hamburgerSpans[2].classList.toggle('-translate-y-1.5');
        });
        
        // Close mobile menu when clicking on a link
        const mobileMenuLinks = document.querySelectorAll('#mobile-menu-dropdown a');
        mobileMenuLinks.forEach(link => {
            link.addEventListener('click', () => {
                // Close dropdown
                mobileMenuDropdown.classList.add('opacity-0', 'invisible', '-translate-y-2');
                mobileMenuDropdown.classList.remove('opacity-100', 'visible', 'translate-y-0');
                
                // Reset hamburger
                hamburgerSpans[0].classList.remove('rotate-45', 'translate-y-1.5');
                hamburgerSpans[1].classList.remove('opacity-0');
                hamburgerSpans[2].classList.remove('-rotate-45', '-translate-y-1.5');
            });
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!mobileMenuToggle.contains(e.target) && !mobileMenuDropdown.contains(e.target)) {
                // Close dropdown
                mobileMenuDropdown.classList.add('opacity-0', 'invisible', '-translate-y-2');
                mobileMenuDropdown.classList.remove('opacity-100', 'visible', 'translate-y-0');
                
                // Reset hamburger
                hamburgerSpans[0].classList.remove('rotate-45', 'translate-y-1.5');
                hamburgerSpans[1].classList.remove('opacity-0');
                hamburgerSpans[2].classList.remove('-rotate-45', '-translate-y-1.5');
            }
        });
        


        // Function to hide indicator smoothly
        function hideIndicator() {
            if (navIndicator) {
                navIndicator.style.opacity = '0';
                navIndicator.style.transition = 'opacity 0.2s ease';
            }
        }
        
        // Clean navigation hover effects - indicator only shows on hover
        let currentHoveredItem = null;
        
        mainNavListItems.forEach(item => {
            item.addEventListener('mouseenter', () => {
                currentHoveredItem = item;
                
                if (navIndicator) {
                    // Show indicator at this item's position
                    navIndicator.style.transition = 'none';
                    navIndicator.style.top = `${item.offsetTop}px`;
                    navIndicator.style.height = `${item.offsetHeight}px`;
                    navIndicator.style.opacity = '1';
                    navIndicator.style.backgroundColor = 'rgba(56, 189, 248, 0.2)';
                    navIndicator.style.boxShadow = '0 0 30px rgba(56, 189, 248, 0.3)';
                    
                    // Re-enable transitions
                    setTimeout(() => {
                        navIndicator.style.transition = 'all 0.3s ease';
                    }, 10);
                }
            });
            
            item.addEventListener('mouseleave', () => {
                currentHoveredItem = null;
                
                if (navIndicator) {
                    // Hide indicator smoothly
                    navIndicator.style.opacity = '0';
                    navIndicator.style.transition = 'opacity 0.2s ease';
                }
            });
        });
        
        // Hide indicator when leaving the entire navigation area
        document.getElementById('main-nav').addEventListener('mouseleave', () => {
            currentHoveredItem = null;
            if (navIndicator) {
                navIndicator.style.opacity = '0';
                navIndicator.style.transition = 'opacity 0.2s ease';
            }
        });

        // --- Enhanced Scroll Detection ---
        
        function updateActiveSection() {
            let current = 'hero';
            const scrollTop = window.pageYOffset;
            const windowHeight = window.innerHeight;
            
            // Simple and reliable section detection
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                const sectionId = section.getAttribute('id');
                
                // Check if the section is currently in the middle of the viewport
                if (scrollTop + windowHeight / 2 >= sectionTop && scrollTop + windowHeight / 2 < sectionTop + sectionHeight) {
                    current = sectionId;
                }
            });

            // Special check for the last section when scrolled to the bottom
            const bottomOfPage = (scrollTop + windowHeight) >= document.body.offsetHeight - 50;
            if (bottomOfPage) {
                current = sections[sections.length - 1].id;
            }

            // Always remove all active classes first, then set only the current one
            mainNavListItems.forEach(li => {
                li.classList.remove('active');
            });
            
            // Set active class only for the current section
            const currentNavItem = document.querySelector(`[data-section="${current}"]`);
            if (currentNavItem) {
                currentNavItem.classList.add('active');
            }
        }

        // Simple and reliable scroll event listener
        window.addEventListener('scroll', () => {
            // Update active section immediately on scroll
            updateActiveSection();
        });
        
        // Also trigger on page load to set initial active state
        document.addEventListener('DOMContentLoaded', () => {
            updateActiveSection();
        });
        
        // Trigger on window resize to handle any layout changes
        window.addEventListener('resize', () => {
            updateActiveSection();
        });



        // --- Enhanced Typing animation with smoother transitions ---
        const typingText = document.getElementById('typing-text');
        const roles = ["Full-Stack Developer", "Software Engineer", "Robotics Enthusiast", "Creative Coder", "Problem Solver"];
        let roleIndex = 0;
        let charIndex = 0;
        let isDeleting = false;

        function type() {
            const currentRole = roles[roleIndex];
            if (isDeleting) {
                typingText.textContent = currentRole.substring(0, charIndex - 1);
                charIndex--;
            } else {
                typingText.textContent = currentRole.substring(0, charIndex + 1);
                charIndex++;
            }

            if (!isDeleting && charIndex === currentRole.length) {
                setTimeout(() => isDeleting = true, 2000);
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                roleIndex = (roleIndex + 1) % roles.length;
            }

            const typeSpeed = isDeleting ? 100 : 200;
            setTimeout(type, typeSpeed);
        }
        document.addEventListener('DOMContentLoaded', type);

        // --- Enhanced Interactive Particle Background ---
        const canvas = document.getElementById('particle-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];
        const mouse = { x: null, y: null, radius: 200 }; // Larger interaction area for black theme

        window.addEventListener('mousemove', (event) => {
            mouse.x = event.x;
            mouse.y = event.y;
        });
        window.addEventListener('mouseout', () => {
            mouse.x = null;
            mouse.y = null;
        });

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 3 + 1;
                this.speedX = Math.random() * 1.5 - 0.75;
                this.speedY = Math.random() * 1.5 - 0.75;
                this.opacity = Math.random() * 0.8 + 0.2;
                this.color = Math.random() > 0.5 ? '#00ffff' : '#0080ff';
            }
            update() {
                if (this.x > canvas.width || this.x < 0) this.speedX *= -1;
                if (this.y > canvas.height || this.y < 0) this.speedY *= -1;
                this.x += this.speedX;
                this.y += this.speedY;
            }
            draw() {
                ctx.fillStyle = this.color;
                ctx.globalAlpha = this.opacity;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
                ctx.globalAlpha = 1;
            }
        }

        function initParticles() {
            particles = [];
            let numberOfParticles = (canvas.width * canvas.height) / 8000; // More particles for black theme
            for (let i = 0; i < numberOfParticles; i++) {
                particles.push(new Particle());
            }
        }

        function connectParticles() {
            let opacityValue = 1;
            for (let a = 0; a < particles.length; a++) {
                // Connect particles to each other
                for (let b = a; b < particles.length; b++) {
                    let distance = Math.sqrt(
                        ((particles[a].x - particles[b].x) * (particles[a].x - particles[b].x))
                        + ((particles[a].y - particles[b].y) * (particles[a].y - particles[b].y))
                    );
                    if (distance < 120) {
                        opacityValue = 1 - (distance/120);
                        ctx.strokeStyle = `rgba(0, 255, 255, ${opacityValue * 0.8})`;
                        ctx.lineWidth = 1.5;
                        ctx.beginPath();
                        ctx.moveTo(particles[a].x, particles[a].y);
                        ctx.lineTo(particles[b].x, particles[b].y);
                        ctx.stroke();
                    }
                }
                // Connect particles to mouse
                if (mouse.x) {
                     let distanceToMouse = Math.sqrt(
                        ((particles[a].x - mouse.x) * (particles[a].x - mouse.x))
                        + ((particles[a].y - mouse.y) * (particles[a].y - mouse.y))
                    );
                    if (distanceToMouse < mouse.radius) {
                        opacityValue = 1 - (distanceToMouse/mouse.radius);
                        ctx.strokeStyle = `rgba(255, 255, 255, ${opacityValue * 1})`;
                        ctx.lineWidth = 2.5;
                        ctx.beginPath();
                        ctx.moveTo(particles[a].x, particles[a].y);
                        ctx.lineTo(mouse.x, mouse.y);
                        ctx.stroke();
                    }
                }
            }
        }

        function animateParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < particles.length; i++) {
                particles[i].update();
                particles[i].draw();
            }
            connectParticles();
            requestAnimationFrame(animateParticles);
        }

        window.addEventListener('resize', () => {
            resizeCanvas();
            initParticles();
        });

        resizeCanvas();
        initParticles();
        animateParticles();

        // --- Enhanced Scroll-triggered animations with Intersection Observer ---
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    
                    // Add staggered animation for child elements
                    const children = entry.target.querySelectorAll('.scroll-fade');
                    children.forEach((child, index) => {
                        setTimeout(() => {
                            child.classList.add('visible');
                        }, index * 100);
                    });
                }
            });
        }, observerOptions);

        document.querySelectorAll('.fade-in-up').forEach(el => {
            observer.observe(el);
        });

        // --- Enhanced Section Title Animation ---
        const titleObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const title = entry.target;
                    if (!title.dataset.animated) {
                        const text = title.textContent;
                        title.innerHTML = '';
                        text.split('').forEach((char, index) => {
                            const span = document.createElement('span');
                            span.textContent = char === ' ' ? '\u00A0' : char;
                            span.style.transitionDelay = `${index * 50}ms`;
                            title.appendChild(span);
                        });
                        title.classList.add('visible');
                        title.dataset.animated = true;
                    }
                    observer.unobserve(title);
                }
            });
        }, { threshold: 0.5 });

        document.querySelectorAll('.section-title').forEach(title => {
            titleObserver.observe(title);
        });

        // --- Enhanced Navigation Smoothness ---
        
        function debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }

        // Smooth scroll to top functionality
        function scrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }

        // Add keyboard navigation support
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Home') {
                e.preventDefault();
                scrollToTop();
            }
        });

        // --- Enhanced Performance with RequestAnimationFrame ---
        function smoothScrollTo(targetY, duration = 1000) {
            const startY = window.pageYOffset;
            const distance = targetY - startY;
            let startTime = null;

            function animation(currentTime) {
                if (startTime === null) startTime = currentTime;
                const timeElapsed = currentTime - startTime;
                const run = easeInOutCubic(timeElapsed, startY, distance, duration);
                window.scrollTo(0, run);
                if (timeElapsed < duration) requestAnimationFrame(animation);
            }

            requestAnimationFrame(animation);
        }

        function easeInOutCubic(t, b, c, d) {
            t /= d / 2;
            if (t < 1) return c / 2 * t * t * t + b;
            t -= 2;
            return c / 2 * (t * t * t + 2) + b;
        }