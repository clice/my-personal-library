(() => {
    const dialog = document.querySelector("#app-modal");
    const content = dialog?.querySelector("[data-modal-content]");

    if (!dialog || !content) {
        return;
    }

    const closeModal = () => {
        if (dialog.open) {
            dialog.close();
        }
    };

    const bindModalContent = () => {
        content.querySelectorAll("[data-modal-close]").forEach((button) => {
            button.addEventListener("click", closeModal);
        });

        const form = content.querySelector("[data-modal-form]");
        if (!form) {
            return;
        }

        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const submitButton = form.querySelector('[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
            }

            try {
                const response = await fetch(form.action, {
                    method: "POST",
                    body: new FormData(form),
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                    },
                });

                const data = await response.json();

                if (data.success) {
                    closeModal();
                    window.location.reload();
                    return;
                }

                if (data.html) {
                    content.innerHTML = data.html;
                    bindModalContent();
                    return;
                }

                throw new Error("Unexpected modal response.");
            } catch (error) {
                console.error(error);
                if (submitButton) {
                    submitButton.disabled = false;
                }
            }
        });
    };

    const openModal = async (url) => {
        content.innerHTML = '<div class="modal-loading">Carregando...</div>';

        if (!dialog.open) {
            dialog.showModal();
        }

        try {
            const response = await fetch(url, {
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            });
            const data = await response.json();
            content.innerHTML = data.html;
            bindModalContent();
        } catch (error) {
            console.error(error);
            closeModal();
            window.location.href = url;
        }
    };

    document.addEventListener("click", (event) => {
        const trigger = event.target.closest("[data-modal-url]");
        if (!trigger) {
            return;
        }

        event.preventDefault();
        openModal(trigger.dataset.modalUrl || trigger.href);
    });

    dialog.addEventListener("click", (event) => {
        if (event.target === dialog) {
            closeModal();
        }
    });

    dialog.addEventListener("cancel", (event) => {
        event.preventDefault();
        closeModal();
    });
})();
