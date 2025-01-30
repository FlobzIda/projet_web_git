/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

import colors from 'vuetify/util/colors'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    themes: {
      light: {
        primary: '#FF5722', // Orange
        secondary: '#607D8B', // Blue grey
        accent: '#8BC34A', // Green accent
        error: '#F44336', // Red
        info: '#2196F3', // Blue
        success: '#4CAF50', // Green
        warning: '#FF9800', // Orange
      },
    },
  },
})
