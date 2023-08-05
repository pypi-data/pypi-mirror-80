function fix_selector_height() {
    $('.selector .selector-chosen').each(function() {
        let selector_chosen = $(this);
        let selector_available = selector_chosen.siblings('.selector-available');

        let selector_chosen_select = selector_chosen.find('select').first();
        let selector_available_select = selector_available.find('select').first();
        let selector_available_filter = selector_available.find('p.selector-filter').first();

        selector_chosen_select.height(selector_available_select.height() + selector_available_filter.outerHeight());
        selector_chosen_select.css('border-top', selector_chosen_select.css('border-bottom'));
    });
}

function handleCarousel($carousel) {
    const errors = $('.errorlist li', $carousel);
    const hash = document.location.hash;

    // If we have errors, open that tab first
    if (errors.length) {
        const errorCarousel = errors.eq(0).closest('.carousel-item').data('carouselid');
        $carousel.carousel(errorCarousel);

    // If we have a tab hash, open that
    } else if (hash) {
        const activeCarousel = $('.carousel-item[data-target="' + hash + '"]', $carousel).data('carouselid');
        $carousel.carousel(activeCarousel);
    }

    // Update page hash/history on slide
    $carousel.on('slide.bs.carousel', function (e) {

        fix_selector_height();

        if (e.relatedTarget.dataset.hasOwnProperty("label")) {
            $('.carousel-fieldset-label', $carousel).text(e.relatedTarget.dataset.label);
        }
        const hash = e.relatedTarget.dataset.target;

        if (history.pushState) {
            history.pushState(null, null, hash);
        } else {
            location.hash = hash;
        }
    });
}

function handleTabs($tabs) {
    const errors = $('.change-form .errorlist li');
    const hash = document.location.hash;

    // If we have errors, open that tab first
    if (errors.length) {
        const tabId = errors.eq(0).closest('.tab-pane').attr('id');
        $('.nav-tabs a[href="#' + tabId + '"]').tab('show');

    // If we have a tab hash, open that
    } else if (hash) {
        $('.nav-tabs a[href="' + hash + '"]', $tabs).tab('show');
    }

    // Change hash for page-reload
    $('.nav-tabs a').on('shown.bs.tab', function (e) {

        fix_selector_height();

        e.preventDefault();
        if (history.pushState) {
            history.pushState(null, null, e.target.hash);
        } else {
            location.hash = e.target.hash;
        }
    });
}

function handleCollapsible($collapsible) {
    const errors = $('.errorlist li', $collapsible);
    const hash = document.location.hash;

    // If we have errors, open that tab first
    if (errors.length) {
        $('.panel-collapse', $collapsible).collapse('hide');
        errors.eq(0).closest('.panel-collapse').collapse('show');

    // If we have a tab hash, open that
    } else if (hash) {
        $('.panel-collapse', $collapsible).collapse('hide');
        $(hash, $collapsible).collapse('show');
    }

    // Change hash for page-reload
    $collapsible.on('shown.bs.collapse', function (e) {

        fix_selector_height();

        if (history.pushState) {
            history.pushState(null, null, '#' + e.target.id);
        } else {
            location.hash = '#' + e.target.id;
        }
    });
}

$(document).ready(function () {
    const $carousel = $('#content-main form #jazzy-carousel');
    const $tabs = $('#content-main form #jazzy-tabs');

    // Ensure all raw_id_fields have the search icon in them
    const $collapsible = $('#content-main form #jazzy-collapsible');
    $('.related-lookup').append('<i class="fa fa-search"></i>');

    // Style the inline fieldset button
    $('.inline-related fieldset.module .add-row a').addClass('btn btn-sm btn-default float-right');

    // Ensure we preserve the tab the user was on using the url hash, even on page reload
    if ($tabs.length) {handleTabs($tabs);}
    else if ($carousel.length) {handleCarousel($carousel);}
    else if ($collapsible.length) {handleCollapsible($collapsible);}
});
