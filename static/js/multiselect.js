(() => {
    const SELECTOR = 'select[data-enhanced-multiselect="true"]';

    const normalize = (value) =>
        value
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .toLowerCase()
            .trim();

    const enhance = (select) => {
        if (select.dataset.enhanced === "true") {
            return;
        }

        select.dataset.enhanced = "true";
        select.classList.add("enhanced-native-select");

        const wrapper = document.createElement("div");
        wrapper.className = "enhanced-multiselect";

        const selectedArea = document.createElement("div");
        selectedArea.className = "enhanced-selected";

        const searchWrap = document.createElement("div");
        searchWrap.className = "enhanced-search-wrap";

        const search = document.createElement("input");
        search.type = "search";
        search.className = "enhanced-search";
        search.autocomplete = "off";
        search.placeholder =
            select.dataset.searchPlaceholder || "Digite para buscar...";

        const dropdown = document.createElement("div");
        dropdown.className = "enhanced-options";
        dropdown.hidden = true;

        searchWrap.append(search);
        wrapper.append(selectedArea, searchWrap, dropdown);
        select.insertAdjacentElement("afterend", wrapper);

        const selectedOptions = () =>
            Array.from(select.options).filter((option) => option.selected);

        const availableOptions = () =>
            Array.from(select.options).filter(
                (option) => option.value && !option.selected
            );

        const renderSelected = () => {
            selectedArea.innerHTML = "";

            selectedOptions().forEach((option) => {
                const chip = document.createElement("span");
                chip.className = "enhanced-chip";

                const label = document.createElement("span");
                label.textContent = option.textContent.trim();

                const remove = document.createElement("button");
                remove.type = "button";
                remove.className = "enhanced-chip-remove";
                remove.setAttribute(
                    "aria-label",
                    `Remover ${option.textContent.trim()}`
                );
                remove.textContent = "×";

                remove.addEventListener("click", () => {
                    option.selected = false;
                    select.dispatchEvent(
                        new Event("change", { bubbles: true })
                    );
                    renderSelected();
                    renderOptions();
                    search.focus();
                });

                chip.append(label, remove);
                selectedArea.append(chip);
            });

            selectedArea.hidden = selectedOptions().length === 0;
        };

        const renderOptions = () => {
            const term = normalize(search.value);
            const matches = availableOptions().filter((option) =>
                normalize(option.textContent).includes(term)
            );

            dropdown.innerHTML = "";

            if (!matches.length) {
                const empty = document.createElement("div");
                empty.className = "enhanced-empty";
                empty.textContent =
                    select.dataset.emptyLabel || "Nenhum resultado encontrado";
                dropdown.append(empty);
                return;
            }

            matches.slice(0, 40).forEach((option) => {
                const button = document.createElement("button");
                button.type = "button";
                button.className = "enhanced-option";
                button.textContent = option.textContent.trim();

                button.addEventListener("click", () => {
                    option.selected = true;
                    select.dispatchEvent(
                        new Event("change", { bubbles: true })
                    );
                    search.value = "";
                    renderSelected();
                    renderOptions();
                    search.focus();
                });

                dropdown.append(button);
            });
        };

        const openDropdown = () => {
            renderOptions();
            dropdown.hidden = false;
            wrapper.classList.add("is-open");
        };

        const closeDropdown = () => {
            dropdown.hidden = true;
            wrapper.classList.remove("is-open");
        };

        search.addEventListener("focus", openDropdown);
        search.addEventListener("input", openDropdown);

        search.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                closeDropdown();
                search.blur();
                return;
            }

            if (event.key === "Enter") {
                const first = dropdown.querySelector(".enhanced-option");
                if (first) {
                    event.preventDefault();
                    first.click();
                }
            }
        });

        document.addEventListener("click", (event) => {
            if (!wrapper.contains(event.target)) {
                closeDropdown();
            }
        });

        renderSelected();
    };

    const init = (root = document) => {
        root.querySelectorAll(SELECTOR).forEach(enhance);
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", () => init());
    } else {
        init();
    }

    document.addEventListener("modal:content-loaded", (event) => {
        init(event.detail?.root || document);
    });
})();
