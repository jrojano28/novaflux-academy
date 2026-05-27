// app/views/static/js/main.js
// Lógica frontend JavaScript interactiva para NovaFlux Academy

document.addEventListener('DOMContentLoaded', () => {

    // ── Lector SPA: alternar lecciones en la barra lateral ──────────
    const lessonButtons = document.querySelectorAll('.lesson-btn');
    const contentBlocks = document.querySelectorAll('.lesson-content-block');

    if (lessonButtons.length > 0) {
        lessonButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetId = button.getAttribute('data-target');

                document.querySelectorAll('.lesson-item').forEach(item => item.classList.remove('active'));
                button.parentElement.classList.add('active');

                contentBlocks.forEach(block => block.classList.remove('active'));
                const targetBlock = document.getElementById(targetId);
                if (targetBlock) targetBlock.classList.add('active');
            });
        });
    }

    // ── Barra de fortaleza de contraseña ────────────────────────────
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

    // ── Flash messages auto-dismiss después de 6 segundos ───────────
    document.querySelectorAll('.flash').forEach(flash => {
        setTimeout(() => {
            flash.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(20px)';
            setTimeout(() => flash.remove(), 500);
        }, 6000);
    });

    // ── Animación de barras de progreso al cargar (dashboard) ────────
    document.querySelectorAll('.progress-bar-fill').forEach(bar => {
        const target = bar.style.width;
        bar.style.width = '0%';
        requestAnimationFrame(() => {
            setTimeout(() => { bar.style.width = target; }, 100);
        });
    });
});
