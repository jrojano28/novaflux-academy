document.addEventListener('DOMContentLoaded', () => {

    const lessonButtons = Array.from(document.querySelectorAll('.lesson-btn'));
    const contentBlocks = document.querySelectorAll('.lesson-content-block');

    if (lessonButtons.length > 0) {
        function activateLessonByIndex(index) {
            if (index < 0 || index >= lessonButtons.length) return;

            const btn = lessonButtons[index];
            const targetId = btn.getAttribute('data-target');

            document.querySelectorAll('.lesson-item').forEach(item => item.classList.remove('active'));
            btn.parentElement.classList.add('active');

            contentBlocks.forEach(block => block.classList.remove('active'));
            const targetBlock = document.getElementById(targetId);
            if (targetBlock) {
                targetBlock.classList.add('active');
                const contentArea = document.querySelector('.content-area');
                if (contentArea) {
                    contentArea.scrollTop = 0;
                }
            }

            updateNavigationButtons(index);

            if (typeof updateLessonRequirements === 'function') {
                setTimeout(() => {
                    updateLessonRequirements();
                }, 50);
            }
        }

        function updateNavigationButtons(currentIndex) {
            const activeBlock = contentBlocks[currentIndex];
            if (!activeBlock) return;

            const prevBtn = activeBlock.querySelector('.btn-prev-lesson');
            const nextBtn = activeBlock.querySelector('.btn-next-lesson');

            if (prevBtn) {
                if (currentIndex === 0) {
                    prevBtn.disabled = true;
                    prevBtn.style.opacity = '0.4';
                    prevBtn.style.cursor = 'not-allowed';
                } else {
                    prevBtn.disabled = false;
                    prevBtn.style.opacity = '1';
                    prevBtn.style.cursor = 'pointer';
                    const newPrevBtn = prevBtn.cloneNode(true);
                    prevBtn.parentNode.replaceChild(newPrevBtn, prevBtn);
                    newPrevBtn.addEventListener('click', () => {
                        activateLessonByIndex(currentIndex - 1);
                    });
                }
            }

            if (nextBtn) {
                if (currentIndex === lessonButtons.length - 1) {
                    nextBtn.disabled = true;
                    nextBtn.style.opacity = '0.4';
                    nextBtn.style.cursor = 'not-allowed';
                } else {
                    nextBtn.disabled = false;
                    nextBtn.style.opacity = '1';
                    nextBtn.style.cursor = 'pointer';
                    const newNextBtn = nextBtn.cloneNode(true);
                    nextBtn.parentNode.replaceChild(newNextBtn, nextBtn);
                    newNextBtn.addEventListener('click', () => {
                        activateLessonByIndex(currentIndex + 1);
                    });
                }
            }
        }

        lessonButtons.forEach((button, index) => {
            button.addEventListener('click', () => {
                activateLessonByIndex(index);
            });
        });

        activateLessonByIndex(0);
    }

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

        setTimeout(() => {
            flash.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(20px)';
            setTimeout(() => flash.remove(), 500);
        }, 6000);
    }

    function showRewardNotification(title, emoji) {
        const container = document.querySelector('.flash-container') || (() => {
            const el = document.createElement('div');
            el.className = 'flash-container';
            document.body.appendChild(el);
            return el;
        })();

        const reward = document.createElement('div');
        reward.className = 'flash flash-reward';
        reward.innerHTML = `
            <div class="reward-content">
                <span class="reward-emoji">${emoji}</span>
                <div>
                    <strong>${title}</strong>
                </div>
            </div>
        `;
        container.appendChild(reward);

        setTimeout(() => {
            reward.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            reward.style.opacity = '0';
            reward.style.transform = 'translateX(20px)';
            setTimeout(() => reward.remove(), 500);
        }, 5000);
    }

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
                { label: 'Muy d\u00e9bil', color: '#f43f5e', width: '15%' },
                { label: 'D\u00e9bil', color: '#f59e0b', width: '35%' },
                { label: 'Aceptable', color: '#eab308', width: '60%' },
                { label: 'Fuerte', color: '#10b981', width: '80%' },
                { label: '\u00a1Muy fuerte!', color: '#00f2fe', width: '100%' }
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

    document.querySelectorAll('.flash').forEach(flash => {
        setTimeout(() => {
            flash.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(20px)';
            setTimeout(() => flash.remove(), 500);
        }, 6000);
    });

    document.querySelectorAll('.progress-bar-fill').forEach(bar => {
        const target = bar.style.width;
        bar.style.width = '0%';
        requestAnimationFrame(() => {
            setTimeout(() => { bar.style.width = target; }, 100);
        });
    });

    const navToggle = document.getElementById('nav-toggle');
    const navLinks = document.getElementById('nav-links');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            navToggle.classList.toggle('active');
            navLinks.classList.toggle('active');
        });

        document.querySelectorAll('.nav-link-item, .nav-btn-logout, .nav-btn-login, .nav-btn-register').forEach(link => {
            link.addEventListener('click', () => {
                navToggle.classList.remove('active');
                navLinks.classList.remove('active');
            });
        });

        document.addEventListener('click', (e) => {
            if (!navLinks.contains(e.target) && !navToggle.contains(e.target)) {
                navToggle.classList.remove('active');
                navLinks.classList.remove('active');
            }
        });
    }

    const sidebarToggleBtn = document.querySelector('.sidebar-toggle-btn');
    const courseSidebar = document.querySelector('.sidebar');

    if (sidebarToggleBtn && courseSidebar) {
        sidebarToggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            courseSidebar.classList.toggle('active');
        });

        document.querySelectorAll('.lesson-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                courseSidebar.classList.remove('active');
            });
        });

        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 768) {
                if (!courseSidebar.contains(e.target) && !sidebarToggleBtn.contains(e.target)) {
                    courseSidebar.classList.remove('active');
                }
            }
        });
    }

    function getActiveLessonBlock() {
        return document.querySelector('.lesson-content-block.active');
    }

    async function fetchLessonRequirements(lessonId) {
        try {
            const response = await fetch(`/courses/lessons/${lessonId}/requirements`);
            const data = await response.json();
            if (data.success) {
                return data.requirements;
            }
        } catch (e) {
            console.error('Error fetching requirements:', e);
        }
        return null;
    }

    async function updateLessonRequirements() {
        const activeBlock = getActiveLessonBlock();
        if (!activeBlock) return;

        const lessonId = activeBlock.getAttribute('data-lesson-id');
        const completeBtn = activeBlock.querySelector('.btn-toggle-complete');
        if (!completeBtn) return;

        const hasQuiz = activeBlock.querySelector('.interactive-quiz') !== null;
        const hasPractice = activeBlock.querySelector('.interactive-practice') !== null;
        const hasSimulator = activeBlock.querySelector('.interactive-simulator') !== null;

        if (!hasQuiz && !hasPractice && !hasSimulator) {
            completeBtn.disabled = false;
            completeBtn.classList.remove('locked-btn');
            const existingCard = activeBlock.querySelector('.lesson-requirements-card');
            if (existingCard) existingCard.remove();
            return;
        }

        const reqs = await fetchLessonRequirements(lessonId);
        if (!reqs) return;

        const quizPassed = reqs.quiz_passed;
        const practicePassed = reqs.practice_completed;
        const simulatorPassed = reqs.simulator_completed;

        let reqCard = activeBlock.querySelector('.lesson-requirements-card');
        if (!reqCard) {
            reqCard = document.createElement('div');
            reqCard.className = 'lesson-requirements-card';
            const completionBox = activeBlock.querySelector('.lesson-completion-box');
            if (completionBox) {
                completionBox.insertBefore(reqCard, completionBox.firstChild);
            }
        }

        let itemsHtml = '';
        let allMet = true;

        if (hasPractice) {
            const metClass = practicePassed ? 'requirement-item met' : 'requirement-item';
            const check = practicePassed ? '✓' : '○';
            itemsHtml += `
                <li class="${metClass}">
                    <div class="requirement-checkbox">${check}</div>
                    <span>✍️ Completa la pr\u00e1ctica de c\u00f3digo manual</span>
                </li>
            `;
            if (!practicePassed) allMet = false;
        }

        if (hasQuiz) {
            const metClass = quizPassed ? 'requirement-item met' : 'requirement-item';
            const check = quizPassed ? '✓' : '○';
            itemsHtml += `
                <li class="${metClass}">
                    <div class="requirement-checkbox">${check}</div>
                    <span>📝 Aprueba el quiz de conocimiento</span>
                </li>
            `;
            if (!quizPassed) allMet = false;
        }

        if (hasSimulator) {
            const metClass = simulatorPassed ? 'requirement-item met' : 'requirement-item';
            const check = simulatorPassed ? '✓' : '○';
            itemsHtml += `
                <li class="${metClass}">
                    <div class="requirement-checkbox">${check}</div>
                    <span>🧬 Realiza la simulaci\u00f3n evolutiva interactiva</span>
                </li>
            `;
            if (!simulatorPassed) allMet = false;
        }

        if (allMet) {
            reqCard.style.borderColor = 'var(--neon-green)';
            reqCard.style.boxShadow = '0 0 20px rgba(16, 185, 129, 0.15)';
            reqCard.innerHTML = `
                <h4 style="color: var(--neon-green); border-color: rgba(16,185,129,0.15)">🏆 \u00a1Todos los requisitos cumplidos!</h4>
                <p style="color: var(--text-muted); font-size: 0.9rem; margin: 0.5rem 0 0 0;">Ya puedes marcar la lecci\u00f3n como completada para desbloquear el siguiente paso.</p>
            `;
            completeBtn.disabled = false;
            completeBtn.classList.remove('locked-btn');
            completeBtn.style.animation = 'pulseLock 2s infinite';
        } else {
            reqCard.style.borderColor = 'var(--neon-cyan)';
            reqCard.style.boxShadow = '0 0 20px rgba(0, 242, 254, 0.08)';
            reqCard.innerHTML = `
                <h4>📋 Requisitos para completar:</h4>
                <ul class="requirements-list">
                    ${itemsHtml}
                </ul>
            `;
            completeBtn.disabled = true;
            completeBtn.classList.add('locked-btn');
            completeBtn.style.animation = 'none';
        }
    }

    const toggleCompleteButtons = document.querySelectorAll('.btn-toggle-complete');

    if (toggleCompleteButtons.length > 0) {
        toggleCompleteButtons.forEach(button => {
            const newBtn = button.cloneNode(true);
            button.parentNode.replaceChild(newBtn, button);

            newBtn.addEventListener('click', () => {
                const contentId = newBtn.getAttribute('data-content-id');

                fetch(`/courses/lessons/${contentId}/toggle-complete`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        if (data.completed) {
                            showRewardNotification('\u00a1Lecci\u00f3n completada y guardada!', '🎉');
                        } else {
                            showFlashMessage('Lecci\u00f3n desmarcada.', 'info');
                        }

                        setTimeout(() => {
                            window.location.reload();
                        }, 1200);
                    } else if (data.requirements_not_met) {
                        showFlashMessage('Completa todos los ejercicios y quizzes primero.', 'error');
                        updateLessonRequirements();
                    } else {
                        showFlashMessage(data.message || 'Error al procesar.', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error al togglear lecci\u00f3n:', error);
                });
            });
        });
    }

    document.querySelectorAll('.btn-playground-run').forEach(button => {
        button.addEventListener('click', () => {
            const container = button.closest('.interactive-playground');
            if (!container) return;
            const editor = container.querySelector('.playground-editor');
            const consoleOutput = container.querySelector('.playground-console-output');
            if (!editor || !consoleOutput) return;
            const code = editor.value;

            consoleOutput.textContent = "Ejecutando ejemplo resuelto...";

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

    document.querySelectorAll('.btn-practice-run').forEach(button => {
        button.addEventListener('click', () => {
            const container = button.closest('.interactive-practice');
            if (!container) return;
            const editor = container.querySelector('.practice-editor');
            const consoleOutput = container.querySelector('.playground-console-output');
            const statusBox = container.querySelector('.practice-validation-status');
            if (!editor || !consoleOutput || !statusBox) return;
            const code = editor.value;

            const expectedOutput = container.getAttribute('data-expected-output') || '';
            const expectedCode = container.getAttribute('data-expected-code') || '';
            const lessonBlock = container.closest('.lesson-content-block');
            const lessonId = lessonBlock ? lessonBlock.getAttribute('data-lesson-id') : '0';

            consoleOutput.textContent = "Ejecutando y validando tu c\u00f3digo...";
            statusBox.className = "practice-validation-status pending";
            statusBox.innerHTML = "⏳ Validando...";

            fetch(`/courses/lessons/${lessonId}/validate-practice`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    code: code,
                    expected_code: expectedCode,
                    expected_output: expectedOutput
                })
            })
            .then(res => res.json())
            .then(data => {
                consoleOutput.textContent = data.output;

                if (data.valid) {
                    statusBox.className = "practice-validation-status success";
                    statusBox.innerHTML = "🎉 \u00a1Ejercicio completado!";
                    showRewardNotification('\u00a1Excelente! Pr\u00e1ctica completada con \u00e9xito.', '🎉');
                    updateLessonRequirements();
                } else {
                    statusBox.className = "practice-validation-status error";
                    statusBox.innerHTML = data.message;
                }
            })
            .catch(err => {
                consoleOutput.textContent = "Error de conexi\u00f3n: " + err;
                statusBox.className = "practice-validation-status error";
                statusBox.innerHTML = "❌ Error de servidor";
            });
        });
    });

    document.querySelectorAll('.interactive-quiz').forEach(quiz => {
        const options = quiz.querySelectorAll('.quiz-option');
        const verifyBtn = quiz.querySelector('.btn-quiz-verify');
        const feedback = quiz.querySelector('.quiz-feedback');
        const lessonBlock = quiz.closest('.lesson-content-block');
        const lessonId = lessonBlock ? lessonBlock.getAttribute('data-lesson-id') : '0';
        const explanationText = quiz.getAttribute('data-explanation') || 'La respuesta correcta se alinea con los fundamentos te\u00f3ricos expuestos en el m\u00f3dulo.';

        options.forEach(opt => {
            opt.addEventListener('click', (e) => {
                options.forEach(o => o.classList.remove('selected'));
                opt.classList.add('selected');
                const radio = opt.querySelector('input[type="radio"]');
                if (radio) radio.checked = true;
            });
        });

        if (verifyBtn && feedback) {
            const newVerifyBtn = verifyBtn.cloneNode(true);
            verifyBtn.parentNode.replaceChild(newVerifyBtn, verifyBtn);

            newVerifyBtn.addEventListener('click', () => {
                let selectedOpt = quiz.querySelector('.quiz-option.selected');

                if (!selectedOpt) {
                    const checkedRadio = quiz.querySelector('input[type="radio"]:checked');
                    if (checkedRadio) {
                        selectedOpt = checkedRadio.closest('.quiz-option');
                        if (selectedOpt) selectedOpt.classList.add('selected');
                    }
                }

                if (!selectedOpt) {
                    feedback.style.display = 'flex';
                    feedback.className = 'quiz-feedback incorrect';
                    feedback.innerHTML = '⚠️ Selecciona primero una opci\u00f3n.';
                    return;
                }

                const isCorrect = selectedOpt.getAttribute('data-correct') === 'true';
                feedback.style.display = 'flex';

                const existingExplanation = quiz.querySelector('.quiz-explanation-box');
                if (existingExplanation) existingExplanation.remove();

                fetch(`/courses/lessons/${lessonId}/validate-quiz`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        correct: isCorrect,
                        explanation: explanationText
                    })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.correct) {
                        feedback.className = 'quiz-feedback correct';
                        feedback.innerHTML = '🎉 \u00a1Correcto! Excelente respuesta.';
                        showRewardNotification('\u00a1Excelente! Cuestionario aprobado.', '🏆');
                        updateLessonRequirements();
                    } else {
                        feedback.className = 'quiz-feedback incorrect';
                        feedback.innerHTML = data.message;

                        const expBox = document.createElement('div');
                        expBox.className = 'quiz-explanation-box';
                        expBox.innerHTML = `
                            <div class="quiz-explanation-title">💡 Explicaci\u00f3n del Concepto:</div>
                            <p>${data.explanation || explanationText}</p>
                            <div class="quiz-retry-hint">
                                <span>🔄 Intentar nuevamente</span>
                            </div>
                        `;
                        quiz.appendChild(expBox);
                        updateLessonRequirements();
                    }
                })
                .catch(err => {
                    feedback.style.display = 'flex';
                    feedback.className = 'quiz-feedback incorrect';
                    feedback.innerHTML = '❌ Error de conexi\u00f3n.';
                });
            });
        }
    });

    const evolverBtn = document.getElementById('btn-evolve-dna');
    const dnaList = document.getElementById('evolve-dna-list');
    const genCounter = document.getElementById('evolve-dna-gen');
    const maxFitnessSpan = document.getElementById('evolve-dna-max-fitness');

    if (evolverBtn && dnaList && genCounter && maxFitnessSpan) {
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

            const lessonBlock = evolverBtn.closest('.lesson-content-block');
            const lessonId = lessonBlock ? lessonBlock.getAttribute('data-lesson-id') : '0';

            fetch(`/courses/lessons/${lessonId}/mark-simulator-done`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            }).catch(e => console.error(e));

            updateLessonRequirements();

            if (population[0].dna === 'BBBB') {
                showRewardNotification('\u00a1Evoluci\u00f3n completada! ADN \u00f3ptimo: BBBB', '🏆');
                evolverBtn.disabled = true;
                evolverBtn.textContent = '🧬 \u00d3ptimo Alcanzado';
            } else {
                showFlashMessage(`🎉 Generaci\u00f3n ${currentGen} creada con \u00e9xito.`, 'info');
            }
        });
    }

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

            showRewardNotification(`\u00a1Ganador del torneo: ${winner.dna}!`, '👑');

            const lessonBlock = runTournamentBtn.closest('.lesson-content-block');
            const lessonId = lessonBlock ? lessonBlock.getAttribute('data-lesson-id') : '0';

            fetch(`/courses/lessons/${lessonId}/mark-simulator-done`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            }).catch(e => console.error(e));

            updateLessonRequirements();
        });
    }

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
                <span class="chromosome-index">Despu\u00e9s:</span>
                <span class="chromosome-dna">🧬 ${mutatedHtml}</span>
                <span class="chromosome-fitness-val" style="color:var(--neon-magenta)">
                    ${flippedCount > 0 ? '⚡ MUTADO (' + flippedCount + ' bits)' : '✕ Sin cambios'}
                </span>
            `;
            mutationList.appendChild(mutCard);

            if (flippedCount > 0) {
                showRewardNotification(`\u00a1Mutaci\u00f3n exitosa! Se alteraron ${flippedCount} genes.`, '⚡');
            } else {
                showFlashMessage('Sin mutaciones en esta tirada azarosa.', 'info');
            }

            const lessonBlock = runMutationBtn.closest('.lesson-content-block');
            const lessonId = lessonBlock ? lessonBlock.getAttribute('data-lesson-id') : '0';

            fetch(`/courses/lessons/${lessonId}/mark-simulator-done`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            }).catch(e => console.error(e));

            updateLessonRequirements();
        });
    }

    setTimeout(() => {
        updateLessonRequirements();
    }, 150);
});
