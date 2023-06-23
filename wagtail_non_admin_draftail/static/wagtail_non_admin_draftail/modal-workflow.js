/* A framework for modal popups that are loaded via AJAX, allowing navigation to other
subpages to happen within the lightbox, and returning a response to the calling page,
possibly after several navigation steps
*/


function NonAdminDraftailModal(el) {
    var modal = $("[role=dialog]", el);

    function listen() {
        var close = $('[data-action="close"]', el);
        if (close) {
            close.on("click", hide);
        }
    }

    function show() {
        el.addClass("open");
        modal.attr("tabindex", 0);
    }

    function hide() {
        el.removeClass("open");
        modal.attr("tabindex", -1);
        // We dispatch this event because Draftail listens to it
        // and releases toolbar from "readonly" state on close.
        $(document.body).trigger("hidden.bs.modal");
    }

    listen();

    return {
        show: show,
        hide: hide
    }
}

function ModalWorkflow(opts) {
    /* options passed in 'opts':
        'url' (required): initial
        'responses' (optional): dict of callbacks to be called when the modal content
            calls modal.respond(callbackName, params)
        'onload' (optional): dict of callbacks to be called when loading a step of the workflow.
            The 'step' field in the response identifies the callback to call, passing it the
            modal object and response data as arguments
    */
    var self = {};
    var responseCallbacks = opts.responses || {};
    var errorCallback = opts.onError || function () {
    };

    /* remove any previous modals before continuing (closing doesn't remove them from the dom) */
    $('body > .Non-Admin-Draftail__modal-wrapper').remove();

// set default contents of container
    var iconClose = '<svg class="icon icon-cross" aria-hidden="true" focusable="false"><use href="#icon-cross"></use></svg>';
    var container = $('<div class="Non-Admin-Draftail__modal-wrapper"><div class="Non-Admin-Draftail__modal" role="dialog" aria-modal="true"><button type="button" data-action="close" class="Non-Admin-Draftail__modal-close" >' + iconClose + "Close" + '</button><div class="Non-Admin-Draftail__modal-body"></div></div></div>');

// add container to body and hide it, so content can be added to it before display
    $('body').append(container);
    var modal = NonAdminDraftailModal(container);

    self.body = container.find('.Non-Admin-Draftail__modal-body');

    self.loadUrl = function (url, urlParams) {
        $.get(url, urlParams, self.loadResponseText, 'text').fail(errorCallback);
    };

    self.postForm = function (url, formData) {
        $.post(url, formData, self.loadResponseText, 'text').fail(errorCallback);
    };

    self.ajaxifyForm = function (formSelector) {
        $(formSelector).each(function () {
            var action = this.action;
            if (this.method.toLowerCase() == 'get') {
                $(this).on('submit', function () {
                    self.loadUrl(action, $(this).serialize());
                    return false;
                });
            } else {
                $(this).on('submit', function () {
                    self.postForm(action, $(this).serialize());
                    return false;
                });
            }
        });
    };

    self.loadResponseText = function (responseText, textStatus, xhr) {
        var response = JSON.parse(responseText);
        self.loadBody(response);
    };

    self.loadBody = function (response) {
        if (response.html) {
            // if response contains an 'html' item, replace modal body with it
            self.body.html(response.html);
            //container.modal('show');
            modal.show();
        }

        /* If response contains a 'step' identifier, and that identifier is found in
        the onload dict, call that onload handler */
        if (opts.onload && response.step && (response.step in opts.onload)) {
            opts.onload[response.step](self, response);
        }
    };

    self.respond = function (responseType) {
        if (responseType in responseCallbacks) {
            var args = Array.prototype.slice.call(arguments, 1);
            responseCallbacks[responseType].apply(self, args);
        }
    };

    self.close = function () {
        modal.hide();
    };

    self.loadUrl(opts.url, opts.urlParams);

    return self;
}
