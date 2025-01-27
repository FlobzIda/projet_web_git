<template>
    <v-stepper v-model="activeStep">
        <v-stepper-items>
            <v-stepper-item :value="1">
                <v-card flat>
                <v-card-title>Étape 1 : Sélectionner le dataset</v-card-title>
                <v-card-actions>
                    <v-btn @click="activeStep = 2">Suivant</v-btn>
                </v-card-actions>
                </v-card>
            </v-stepper-item>

            <v-stepper-item :value="2">
                <v-card flat>
                <v-card-title>Étape 2 : Sélectionner les colonnes</v-card-title>
                <v-card-actions>
                    <v-btn @click="activeStep = 1">Précédent</v-btn>
                    <v-btn @click="activeStep = 3">Suivant</v-btn>
                </v-card-actions>
                </v-card>
            </v-stepper-item>

            <v-stepper-item :value="3">
                <v-card flat>
                <v-card-title>Étape 3 : Sélectionner le modèle</v-card-title>
                <v-card-actions>
                    <v-btn @click="activeStep = 2">Précédent</v-btn>
                </v-card-actions>
                </v-card>
            </v-stepper-item>
        </v-stepper-items>
    </v-stepper>
</template>

<script>
// import { VFileUpload } from 'vuetify/labs/VFileUpload'

export default {
    data() {
        return {
            dataset : {},
            activeStep : 1
        };
    }
}
</script>


<!-- <v-select
clearable
label="Selectionnez les variables en x"
:items="['x', 'xx', 'xxx', 'xxx']">
</v-select>
<v-select
clearable
label="Selecttionnez les variables en y"
:items="['y', 'yy', 'yyy']"
multiple>

</v-select> -->

<!-- <VFileUpload
    label="Upload your files"
    multiple
    v-model="files"/> -->