// app/views/static/js/main.js
// Lógica frontend JavaScript interactiva para NovaFlux Academy

document.addEventListener('DOMContentLoaded', () => {

    // ── Lector SPA: Alternar lecciones en la barra lateral e inicializar navegación ──
    const lessonButtons = Array.from(document.querySelectorAll('.lesson-btn'));
    const contentBlocks = document.querySelectorAll('.lesson-content-block');

    if (lessonButtons.length > 0) {
        // Función para activar una lección específica por su índice
        function activateLessonByIndex(index) {
            if (index < 0 || index >= lessonButtons.length) return;
            
            const btn = lessonButtons[index];
            const targetId = btn.getAttribute('data-target');

            // Quitar clase activa de todos los ítems y añadir al seleccionado
            document.querySelectorAll('.lesson-item').forEach(item => item.classList.remove('active'));
            btn.parentElement.classList.add('active');

            // Quitar clase activa de todos los bloques de contenido y activar el objetivo
            contentBlocks.forEach(block => block.classList.remove('active'));
            const targetBlock = document.getElementById(targetId);
            if (targetBlock) {
                targetBlock.classList.add('active');
                
                // Hacer scroll del panel de lectura hacia arriba
                const contentArea = document.querySelector('.content-area');
                if (contentArea) {
                    contentArea.scrollTop = 0;
                }
            }

            // Actualizar el estado de los botones de navegación secuencial
            updateNavigationButtons(index);
        }

        // Función para actualizar y configurar los botones "Anterior" y "Siguiente"
        function updateNavigationButtons(currentIndex) {
            const activeBlock = contentBlocks[currentIndex];
            if (!activeBlock) return;

            const prevBtn = activeBlock.querySelector('.btn-prev-lesson');
            const nextBtn = activeBlock.querySelector('.btn-next-lesson');

            // Botón Anterior
            if (prevBtn) {
                if (currentIndex === 0) {
                    prevBtn.disabled = true;
                    prevBtn.style.opacity = '0.4';
                    prevBtn.style.cursor = 'not-allowed';
                } else {
                    prevBtn.disabled = false;
                    prevBtn.style.opacity = '1';
                    prevBtn.style.cursor = 'pointer';
                    // Clonar para limpiar event listeners previos
                    const newPrevBtn = prevBtn.cloneNode(true);
                    prevBtn.parentNode.replaceChild(newPrevBtn, prevBtn);
                    newPrevBtn.addEventListener('click', () => {
                        activateLessonByIndex(currentIndex - 1);
                    });
                }
            }

            // Botón Siguiente
            if (nextBtn) {
                if (currentIndex === lessonButtons.length - 1) {
                    nextBtn.disabled = true;
                    nextBtn.style.opacity = '0.4';
                    nextBtn.style.cursor = 'not-allowed';
                } else {
                    nextBtn.disabled = false;
                    nextBtn.style.opacity = '1';
                    nextBtn.style.cursor = 'pointer';
                    // Clonar para limpiar event listeners previos
                    const newNextBtn = nextBtn.cloneNode(true);
                    nextBtn.parentNode.replaceChild(newNextBtn, nextBtn);
                    newNextBtn.addEventListener('click', () => {
                        activateLessonByIndex(currentIndex + 1);
                    });
                }
            }
        }

        // Registrar eventos click en los botones de la barra lateral
        lessonButtons.forEach((button, index) => {
            button.addEventListener('click', () => {
                activateLessonByIndex(index);
            });
        });

        // Inicializar el lector activando la primera lección por defecto
        activateLessonByIndex(0);
    }

    // ── Lógica AJAX para Completar/Desmarcar Lecciones ──
    const toggleCompleteButtons = document.querySelectorAll('.btn-toggle-complete');

    if (toggleCompleteButtons.length > 0) {
        toggleCompleteButtons.forEach(button => {
            button.addEventListener('click', () => {
                const contentId = button.getAttribute('data-content-id');
                
                // Enviar petición POST vía AJAX
                fetch(`/courses/lessons/${contentId}/toggle-complete`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // 1. Actualizar estilos del botón
                        if (data.completed) {
                            button.classList.add('completed');
                            button.textContent = '✓ Lección Completada';
                            button.style.background = 'rgba(16, 185, 129, 0.15)';
                            button.style.color = 'var(--neon-green)';
                            button.style.border = '1px solid var(--neon-green)';
                            button.style.boxShadow = '0 0 15px rgba(16, 185, 129, 0.2)';
                        } else {
                            button.classList.remove('completed');
                            button.textContent = 'Marcar como Completada';
                            button.style.background = 'transparent';
                            button.style.color = 'var(--text-main)';
                            button.style.border = '1px solid rgba(255, 255, 255, 0.2)';
                            button.style.boxShadow = 'none';
                        }

                        // 2. Actualizar el checkmark de la barra lateral
                        const sidebarItem = document.getElementById(`sidebar-item-${contentId}`);
                        if (sidebarItem) {
                            const checkmark = sidebarItem.querySelector('.sidebar-checkmark');
                            if (checkmark) {
                                if (data.completed) {
                                    sidebarItem.classList.add('completed-item');
                                    checkmark.textContent = '✓';
                                    checkmark.style.opacity = '1';
                                } else {
                                    sidebarItem.classList.remove('completed-item');
                                    checkmark.textContent = '○';
                                    checkmark.style.opacity = '0.2';
                                }
                            }
                        }

                        // 3. Actualizar la barra de progreso del curso (si existe)
                        const progressBarFill = document.getElementById('course-progress-bar');
                        const progressPercentVal = document.getElementById('progress-percent-val');
                        if (progressBarFill) {
                            progressBarFill.style.width = `${data.progress}%`;
                        }
                        if (progressPercentVal) {
                            progressPercentVal.textContent = Math.round(data.progress);
                        }

                        // 4. Lanzar notificación flotante si el curso se completó recién
                        if (data.course_newly_completed) {
                            showFlashMessage('¡Felicidades! Has completado el 100% de este curso. Revisa tu Dashboard.', 'success');
                        }
                    }
                })
                .catch(error => {
                    console.error('Error al togglear el completado de lección:', error);
                });
            });
        });
    }

    // Función auxiliar para renderizar mensajes flash dinámicos
    function showFlashMessage(message, category) {
        const container = document.querySelector('.flash-container') || (() => {
            const el = document.createElement('div');
            el.className = 'flash-container';
            document.body.appendChild(el);
            return el;
        })();

        const flash = document.createElement('div');
        flash.className = `flash flash-${category}`;
        flash.innerHTML = `
            <span>${message}</span>
            <button onclick="this.parentElement.remove()">✕</button>
        `;
        container.appendChild(flash);

        // Auto-dismiss en 6 segundos
        setTimeout(() => {
            flash.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(20px)';
            setTimeout(() => flash.remove(), 500);
        }, 6000);
    }

    // ── Barra de fortaleza de contraseña ──
    const passwordInput = document.getElementById('password');
    const strengthFill = document.getElementById('strength-fill');
    const strengthLabel = document.getElementById('strength-label');

    if (passwordInput && strengthFill) {
        passwordInput.addEventListener('input', () => {
            const pwd = passwordInput.value;
            let strength = 0;
            if (pwd.length >= 8) strength++;
            if (/[A-Z]/.test(pwd)) strength++;
            if (/[0-9]/.test(pwd)) strength++;
            if (/[^A-Za-z0-9]/.test(pwd)) strength++;

            const levels = [
                { label: 'Muy débil', color: '#f43f5e', width: '15%' },
                { label: 'Débil', color: '#f59e0b', width: '35%' },
                { label: 'Aceptable', color: '#eab308', width: '60%' },
                { label: 'Fuerte', color: '#10b981', width: '80%' },
                { label: '¡Muy fuerte!', color: '#00f2fe', width: '100%' }
            ];

            const level = levels[Math.min(strength, 4)];
            strengthFill.style.width = pwd.length === 0 ? '0%' : level.width;
            strengthFill.style.background = level.color;
            if (strengthLabel) {
                strengthLabel.textContent = pwd.length === 0 ? '' : level.label;
                strengthLabel.style.color = level.color;
            }
        });
    }

    // ── Flash messages auto-dismiss después de 6 segundos ──
    document.querySelectorAll('.flash').forEach(flash => {
        setTimeout(() => {
            flash.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(20px)';
            setTimeout(() => flash.remove(), 500);
        }, 6000);
    });

    // ── Animación de barras de progreso al cargar (dashboard) ──
    document.querySelectorAll('.progress-bar-fill').forEach(bar => {
        const target = bar.style.width;
        bar.style.width = '0%';
        requestAnimationFrame(() => {
            setTimeout(() => { bar.style.width = target; }, 100);
        });
    });
});
