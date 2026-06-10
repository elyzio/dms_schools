/*
 * Dependent dropdown cascade for Distrito -> Subdistrito -> Suco -> Aldeia.
 * Used on Estudante and Professor forms (same address fields/IDs).
 */
(function () {
    var PLACEHOLDER = '---------';

    function populate(select, items, valueKey, labelKey, selectedId) {
        select.innerHTML = '';
        var placeholder = document.createElement('option');
        placeholder.value = '';
        placeholder.textContent = PLACEHOLDER;
        select.appendChild(placeholder);
        items.forEach(function (item) {
            var option = document.createElement('option');
            option.value = item[valueKey];
            option.textContent = item[labelKey];
            if (selectedId && String(item[valueKey]) === String(selectedId)) {
                option.selected = true;
            }
            select.appendChild(option);
        });
        select.disabled = items.length === 0;
    }

    function fetchOptions(url, param, id) {
        if (!id) {
            return Promise.resolve([]);
        }
        return fetch(url + '?' + param + '=' + encodeURIComponent(id))
            .then(function (response) { return response.ok ? response.json() : []; });
    }

    window.setupAddressCascade = function (config) {
        var distritoEl = document.getElementById(config.distrito);
        var subdistritoEl = document.getElementById(config.subdistrito);
        var sucoEl = document.getElementById(config.suco);
        var aldeiaEl = document.getElementById(config.aldeia);

        if (!distritoEl || !subdistritoEl || !sucoEl || !aldeiaEl) {
            return;
        }

        var urls = config.urls;

        function loadSubdistritos(distritoId, selectedId) {
            return fetchOptions(urls.subdistritos, 'distrito_id', distritoId).then(function (items) {
                populate(subdistritoEl, items, 'id', 'subdistrito', selectedId);
            });
        }

        function loadSucos(subdistritoId, selectedId) {
            return fetchOptions(urls.sucos, 'subdistrito_id', subdistritoId).then(function (items) {
                populate(sucoEl, items, 'id', 'suco', selectedId);
            });
        }

        function loadAldeias(sucoId, selectedId) {
            return fetchOptions(urls.aldeias, 'suco_id', sucoId).then(function (items) {
                populate(aldeiaEl, items, 'id', 'aldeia', selectedId);
            });
        }

        // Preserve values Django pre-selected on edit forms, then clear the
        // dependent dropdowns so nothing shows until their parent is chosen.
        var initialSubdistrito = subdistritoEl.value;
        var initialSuco = sucoEl.value;
        var initialAldeia = aldeiaEl.value;

        populate(subdistritoEl, [], 'id', 'subdistrito', null);
        populate(sucoEl, [], 'id', 'suco', null);
        populate(aldeiaEl, [], 'id', 'aldeia', null);

        if (distritoEl.value) {
            loadSubdistritos(distritoEl.value, initialSubdistrito).then(function () {
                if (!initialSubdistrito) {
                    return;
                }
                return loadSucos(initialSubdistrito, initialSuco).then(function () {
                    if (initialSuco) {
                        return loadAldeias(initialSuco, initialAldeia);
                    }
                });
            });
        }

        distritoEl.addEventListener('change', function () {
            populate(sucoEl, [], 'id', 'suco', null);
            populate(aldeiaEl, [], 'id', 'aldeia', null);
            if (this.value) {
                loadSubdistritos(this.value, null);
            } else {
                populate(subdistritoEl, [], 'id', 'subdistrito', null);
            }
        });

        subdistritoEl.addEventListener('change', function () {
            populate(aldeiaEl, [], 'id', 'aldeia', null);
            if (this.value) {
                loadSucos(this.value, null);
            } else {
                populate(sucoEl, [], 'id', 'suco', null);
            }
        });

        sucoEl.addEventListener('change', function () {
            if (this.value) {
                loadAldeias(this.value, null);
            } else {
                populate(aldeiaEl, [], 'id', 'aldeia', null);
            }
        });
    };
})();
