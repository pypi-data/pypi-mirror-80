"use strict";
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", { value: true });
const coreutils_1 = require("@phosphor/coreutils");
const dataWidgets = require("jupyter-datawidgets");
const base_1 = require("@jupyter-widgets/base");
const EXTENSION_ID = 'jupyter.extensions.datawidgets';
/**
 * The token identifying the JupyterLab plugin.
 */
exports.IDataWidgetsExtension = new coreutils_1.Token(EXTENSION_ID);
;
/**
 * The notebook diff provider.
 */
const dataWidgetsProvider = {
    id: EXTENSION_ID,
    requires: [base_1.IJupyterWidgetRegistry],
    activate: activateWidgetExtension,
    autoStart: true
}; // TODO: Remove once we drop support for lab < 2
exports.default = dataWidgetsProvider;
/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app, widgetsManager) {
    widgetsManager.registerWidget({
        name: 'jupyter-datawidgets',
        version: dataWidgets.version,
        exports: dataWidgets
    });
    return {};
}
//# sourceMappingURL=index.js.map