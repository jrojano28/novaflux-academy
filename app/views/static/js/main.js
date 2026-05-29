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
<<<<<<< Updated upstream:app/views/static/js/main.js
=======

    // ── Menú hamburguesa móvil interactivo ──
    const navToggle = document.getElementById('nav-toggle');
    const navLinks = document.getElementById('nav-links');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            navToggle.classList.toggle('active');
            navLinks.classList.toggle('active');
        });

        // Cerrar menú al hacer clic en cualquier enlace
        document.querySelectorAll('.nav-link-item, .nav-btn-logout, .nav-btn-login, .nav-btn-register').forEach(link => {
            link.addEventListener('click', () => {
                navToggle.classList.remove('active');
                navLinks.classList.remove('active');
            });
        });

        // Cerrar al hacer clic fuera del menú
        document.addEventListener('click', (e) => {
            if (!navLinks.contains(e.target) && !navToggle.contains(e.target)) {
                navToggle.classList.remove('active');
                navLinks.classList.remove('active');
            }
        });
    }

    // ── Toggler de la barra lateral (Syllabus de Lecciones) en Móvil ──
    const sidebarToggleBtn = document.getElementById('sidebar-toggle-btn');
    const courseSidebar = document.getElementById('course-sidebar');

    if (sidebarToggleBtn && courseSidebar) {
        sidebarToggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            courseSidebar.classList.toggle('active');
        });

        // Cerrar sidebar al seleccionar una lección
        document.querySelectorAll('.lesson-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                courseSidebar.classList.remove('active');
            });
        });

        // Cerrar al hacer clic fuera del sidebar en móvil
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 768) {
                if (!courseSidebar.contains(e.target) && !sidebarToggleBtn.contains(e.target)) {
                    courseSidebar.classList.remove('active');
                }
            }
        });
    }

    // ── PLAYGROUND DE PYTHON SIMPLE (AJAX) ──
    document.querySelectorAll('.btn-playground-run').forEach(button => {
        button.addEventListener('click', () => {
            const container = button.closest('.interactive-playground');
            const editor = container.querySelector('.playground-editor');
            const consoleOutput = container.querySelector('.playground-console-output');
            const code = editor.value;

            consoleOutput.textContent = "Ejecutando código en servidor...";

            fetch('/courses/run-code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ code: code })
            })
            .then(res => res.json())
            .then(data => {
                consoleOutput.textContent = data.output;
            })
            .catch(err => {
                consoleOutput.textContent = "Error al conectar con el servidor: " + err;
            });
        });
    });

    // ── QUIZZES DINÁMICOS E INTERACTIVOS ──
    document.querySelectorAll('.interactive-quiz').forEach(quiz => {
        const options = quiz.querySelectorAll('.quiz-option');
        const verifyBtn = quiz.querySelector('.btn-quiz-verify');
        const feedback = quiz.querySelector('.quiz-feedback');

        options.forEach(opt => {
            opt.addEventListener('click', () => {
                options.forEach(o => o.classList.remove('selected'));
                opt.classList.add('selected');
                const radio = opt.querySelector('input[type="radio"]');
                if (radio) radio.checked = true;
            });
        });

        if (verifyBtn) {
            verifyBtn.addEventListener('click', () => {
                const selectedOpt = quiz.querySelector('.quiz-option.selected');
                if (!selectedOpt) {
                    feedback.style.display = 'flex';
                    feedback.className = 'quiz-feedback incorrect';
                    feedback.innerHTML = '⚠️ Selecciona primero una opción.';
                    return;
                }

                const isCorrect = selectedOpt.getAttribute('data-correct') === 'true';
                feedback.style.display = 'flex';

                if (isCorrect) {
                    feedback.className = 'quiz-feedback correct';
                    feedback.innerHTML = '🎉 ¡Correcto! Excelente respuesta.';
                    showFlashMessage('🎉 ¡Excelente! Práctica de quiz completada.', 'success');
                } else {
                    feedback.className = 'quiz-feedback incorrect';
                    feedback.innerHTML = '❌ Incorrecto. ¡Vuelve a intentarlo!';
                }
            });
        }
    });

    // ── SIMULADOR DE EVOLUCIÓN GENÉTICA (Módulo 2) ──
    const evolverBtn = document.getElementById('btn-evolve-dna');
    const dnaList = document.getElementById('evolve-dna-list');
    const genCounter = document.getElementById('evolve-dna-gen');
    const maxFitnessSpan = document.getElementById('evolve-dna-max-fitness');

    if (evolverBtn && dnaList) {
        let currentGen = 1;
        let population = [
            { dna: 'AABB', fitness: 2 },
            { dna: 'ABAB', fitness: 2 },
            { dna: 'BBAA', fitness: 2 },
            { dna: 'AAAA', fitness: 4 }
        ];

        function calculateFitness(dna) {
            let fit = 0;
            for (let i = 0; i < dna.length; i++) {
                if (dna[i] === 'B') fit++;
            }
            return fit;
        }

        evolverBtn.addEventListener('click', () => {
            currentGen++;
            genCounter.textContent = currentGen;

            // Simulación simplificada client-side
            population.sort((a,b) => b.fitness - a.fitness);
            let parents = [population[0].dna, population[1].dna];

            let newPop = [];
            for (let i = 0; i < 4; i++) {
                let crossoverPoint = Math.floor(Math.random() * 3) + 1;
                let childDna = parents[0].substring(0, crossoverPoint) + parents[1].substring(crossoverPoint);

                if (Math.random() < 0.5) {
                    let mutateIdx = Math.floor(Math.random() * 4);
                    let char = Math.random() < 0.8 ? 'B' : 'A';
                    childDna = childDna.substring(0, mutateIdx) + char + childDna.substring(mutateIdx + 1);
                }

                newPop.push({
                    dna: childDna,
                    fitness: calculateFitness(childDna)
                });
            }

            population = newPop;
            population.sort((a,b) => b.fitness - a.fitness);

            dnaList.innerHTML = '';
            population.forEach((ind, index) => {
                let dnaHtml = '';
                for (let i = 0; i < ind.dna.length; i++) {
                    let charClass = ind.dna[i] === 'B' ? 'dna-char mutated' : 'dna-char';
                    dnaHtml += `<span class="${charClass}">${ind.dna[i]}</span>`;
                }

                const card = document.createElement('div');
                card.className = 'chromosome-card-visual';
                card.innerHTML = `
                    <span class="chromosome-index">Indiv. ${index+1}</span>
                    <span class="chromosome-dna">🧬 ${dnaHtml}</span>
                    <span class="chromosome-fitness-val">Aptitud: ${ind.fitness}/4</span>
                `;
                dnaList.appendChild(card);
            });

            maxFitnessSpan.textContent = population[0].fitness;

            if (population[0].dna === 'BBBB') {
                showFlashMessage('🏆 ¡Evolución completada! Has alcanzado el ADN óptimo: BBBB', 'success');
                evolverBtn.disabled = true;
                evolverBtn.textContent = '🧬 Óptimo Alcanzado';
            } else {
                showFlashMessage(`🎉 Generación ${currentGen} creada con éxito.`, 'info');
            }
        });
    }

    // ── SIMULADOR DE SELECCIÓN POR TORNEO (Módulo 5) ──
    const runTournamentBtn = document.getElementById('btn-run-tournament');
    const tournamentList = document.getElementById('tournament-dna-list');

    if (runTournamentBtn && tournamentList) {
        runTournamentBtn.addEventListener('click', () => {
            const sizeInput = document.getElementById('tournament-size-input');
            const k = parseInt(sizeInput ? sizeInput.value : 3) || 3;

            const pool = [
                { dna: 'AABB', fitness: 2 },
                { dna: 'ABAB', fitness: 2 },
                { dna: 'AAAA', fitness: 0 },
                { dna: 'BBBB', fitness: 4 },
                { dna: 'BABA', fitness: 2 },
                { dna: 'BBAB', fitness: 3 },
                { dna: 'AAAB', fitness: 1 }
            ];

            let contenders = [];
            let poolCopy = [...pool];
            for (let i = 0; i < Math.min(k, pool.length); i++) {
                let rIdx = Math.floor(Math.random() * poolCopy.length);
                contenders.push(poolCopy.splice(rIdx, 1)[0]);
            }

            contenders.sort((a,b) => b.fitness - a.fitness);
            let winner = contenders[0];

            tournamentList.innerHTML = '';
            contenders.forEach((ind, index) => {
                const isWinner = ind.dna === winner.dna;
                const card = document.createElement('div');
                card.className = 'chromosome-card-visual';
                if (isWinner) {
                    card.style.borderColor = 'var(--neon-green)';
                    card.style.background = 'rgba(16, 185, 129, 0.08)';
                }
                card.innerHTML = `
                    <span class="chromosome-index">Contend. ${index+1}</span>
                    <span class="chromosome-dna">🧬 ${ind.dna}</span>
                    <span class="chromosome-fitness-val" style="color: ${isWinner ? 'var(--neon-green)' : 'var(--text-muted)'}">
                        ${isWinner ? '👑 GANADOR (Aptitud: ' + ind.fitness + ')' : 'Aptitud: ' + ind.fitness}
                    </span>
                `;
                tournamentList.appendChild(card);
            });

            showFlashMessage(`👑 ¡Ganador del torneo: ${winner.dna}!`, 'success');
        });
    }

    // ── SIMULADOR DE MUTACIÓN FLIP-BIT (Módulo 7) ──
    const runMutationBtn = document.getElementById('btn-run-mutation');
    const mutationList = document.getElementById('mutation-dna-list');

    if (runMutationBtn && mutationList) {
        runMutationBtn.addEventListener('click', () => {
            const inputEl = document.getElementById('mutation-input-dna');
            const rateEl = document.getElementById('mutation-rate-input');
            
            let dna = (inputEl ? inputEl.value : '10101010').trim() || '10101010';
            let rate = parseFloat(rateEl ? rateEl.value : 0.2) || 0.2;

            let originalHtml = '';
            let mutatedHtml = '';
            let flippedCount = 0;

            for (let i = 0; i < dna.length; i++) {
                let char = dna[i];
                if (char !== '0' && char !== '1') char = '0';
                originalHtml += `<span class="dna-char">${char}</span>`;

                if (Math.random() < rate) {
                    let mutatedChar = char === '0' ? '1' : '0';
                    mutatedHtml += `<span class="dna-char mutated">${mutatedChar}</span>`;
                    flippedCount++;
                } else {
                    mutatedHtml += `<span class="dna-char">${char}</span>`;
                }
            }

            mutationList.innerHTML = '';
            
            const origCard = document.createElement('div');
            origCard.className = 'chromosome-card-visual';
            origCard.innerHTML = `
                <span class="chromosome-index">Antes:</span>
                <span class="chromosome-dna">🧬 ${originalHtml}</span>
                <span class="chromosome-fitness-val" style="color:var(--neon-cyan)">Original</span>
            `;
            mutationList.appendChild(origCard);

            const mutCard = document.createElement('div');
            mutCard.className = 'chromosome-card-visual';
            mutCard.innerHTML = `
                <span class="chromosome-index">Después:</span>
                <span class="chromosome-dna">🧬 ${mutatedHtml}</span>
                <span class="chromosome-fitness-val" style="color:var(--neon-magenta)">
                    ${flippedCount > 0 ? '⚡ MUTADO (' + flippedCount + ' bits)' : '✕ Sin cambios'}
                </span>
            `;
            mutationList.appendChild(mutCard);

            if (flippedCount > 0) {
                showFlashMessage(`⚡ Mutación exitosa. Se han alterado ${flippedCount} genes.`, 'success');
            } else {
                showFlashMessage('Sin mutaciones en esta tirada azarosa.', 'info');
            }
        });
    }
>>>>>>> Stashed changes:app/static/js/main.js
});
