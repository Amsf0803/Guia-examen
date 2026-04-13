document.addEventListener('DOMContentLoaded', () => {
    // 1. Inyectar HTML del Lightbox si no existe
    if (!document.getElementById('global-lightbox')) {
        const lightboxHTML = `
        <div id="global-lightbox" class="lightbox-modal">
            <div class="lightbox-top-controls">
                <button class="lb-theme-btn lb-theme-dark" title="Fondo Oscuro"></button>
                <button class="lb-theme-btn lb-theme-gray" title="Fondo Gris"></button>
                <button class="lb-theme-btn lb-theme-light" title="Fondo Claro"></button>
                <button class="lb-btn lb-close" title="Cerrar">&times;</button>
            </div>
            
            <div class="lightbox-content-wrapper">
                <img id="global-lightbox-img" class="lightbox-img" src="" alt="Vista ampliada">
            </div>

            <div class="lightbox-controls">
                <button class="lb-btn" id="lb-zoom-out" title="Alejar (-)">-</button>
                <span id="lb-zoom-level" style="color:white; font-weight:bold; min-width:50px; text-align:center;">100%</span>
                <button class="lb-btn" id="lb-zoom-in" title="Acercar (+)">+</button>
            </div>
        </div>
        `;
        document.body.insertAdjacentHTML('beforeend', lightboxHTML);
    }

    const modal = document.getElementById('global-lightbox');
    const modalImg = document.getElementById('global-lightbox-img');
    const closeBtn = modal.querySelector('.lb-close');
    const zoomInBtn = document.getElementById('lb-zoom-in');
    const zoomOutBtn = document.getElementById('lb-zoom-out');
    const zoomLevelTxt = document.getElementById('lb-zoom-level');
    
    const themeDark = modal.querySelector('.lb-theme-dark');
    const themeGray = modal.querySelector('.lb-theme-gray');
    const themeLight = modal.querySelector('.lb-theme-light');

    let currentZoom = 1;
    const ZOOM_SPEED = 0.1;
    const MAX_ZOOM = 5;
    const MIN_ZOOM = 0.5;

    let isDragging = false;
    let startX, startY;
    let translateX = 0, translateY = 0;

    // --- Funciones Core ---
    function openLightbox(src) {
        modalImg.src = src;
        currentZoom = 1;
        translateX = 0;
        translateY = 0;
        updateTransform();
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevenir scroll fondo
    }

    function closeLightbox() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
        setTimeout(() => { modalImg.src = ''; }, 300);
    }

    function updateTransform() {
        modalImg.style.transform = `translate(${translateX}px, ${translateY}px) scale(${currentZoom})`;
        zoomLevelTxt.textContent = Math.round(currentZoom * 100) + '%';
    }

    function changeZoom(delta) {
        currentZoom += delta;
        currentZoom = Math.max(MIN_ZOOM, Math.min(MAX_ZOOM, currentZoom));
        updateTransform();
    }

    // --- Event Listeners ---

    // Cerrar al clickear afuera o botón
    closeBtn.addEventListener('click', closeLightbox);
    modal.addEventListener('click', (e) => {
        if (e.target === modal || e.target.classList.contains('lightbox-content-wrapper')) {
            closeLightbox();
        }
    });

    // Cerrar con Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeLightbox();
        }
    });

    // Zoom con Botones
    zoomInBtn.addEventListener('click', () => changeZoom(ZOOM_SPEED * 2));
    zoomOutBtn.addEventListener('click', () => changeZoom(-ZOOM_SPEED * 2));

    // Zoom con Rueda
    modal.addEventListener('wheel', (e) => {
        e.preventDefault();
        const delta = e.deltaY < 0 ? ZOOM_SPEED : -ZOOM_SPEED;
        changeZoom(delta);
    }, { passive: false });

    // Drag (Paneo) de la imagen
    modalImg.addEventListener('mousedown', (e) => {
        e.preventDefault();
        isDragging = true;
        startX = e.clientX - translateX;
        startY = e.clientY - translateY;
    });

    window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        translateX = e.clientX - startX;
        translateY = e.clientY - startY;
        updateTransform();
    });

    window.addEventListener('mouseup', () => {
        isDragging = false;
    });

    // Temas de Fondo
    themeDark.addEventListener('click', () => {
        modal.className = 'lightbox-modal active bg-dark';
    });
    themeGray.addEventListener('click', () => {
        modal.className = 'lightbox-modal active bg-gray';
    });
    themeLight.addEventListener('click', () => {
        modal.className = 'lightbox-modal active bg-light';
    });

    // --- Attach a Todas las Imágenes ---
    // Buscar la forma de adjuntar el click a cualquier imagen (excepto header/logos)
    const attachImages = () => {
        const images = document.querySelectorAll('img:not(.no-zoom)');
        images.forEach(img => {
            // Ignorar logos basándonos en si están dentro de un header o por el src
            if (img.closest('header') || img.src.includes('logo') || img.src.includes('LIA')) {
                img.classList.add('no-zoom');
                img.style.cursor = 'default';
                return;
            }
            
            // Adjuntar evento si no lo tiene
            if (!img.dataset.lightboxAttached) {
                img.dataset.lightboxAttached = "true";
                img.addEventListener('click', () => {
                    openLightbox(img.src);
                });
            }
        });
    };

    attachImages();

    // Observador para adjuntar eventos a imágenes generadas dinámicamente
    // Útil si hay carga por ajax o manipulaciones DOM (aunque Jinja pre-renderiza, sirve de respaldo)
    const observer = new MutationObserver((mutations) => {
        let shouldAttach = false;
        mutations.forEach(m => {
            if (m.addedNodes.length) shouldAttach = true;
        });
        if (shouldAttach) attachImages();
    });
    observer.observe(document.body, { childList: true, subtree: true });
});
