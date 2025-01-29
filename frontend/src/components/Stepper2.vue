<template>
    <v-stepper
        v-model="activeStep"
        hide-actions
        prev-text=""
        next-text=""
        :items="['Step 1', 'Step 2', 'Step 3']"

        
    >
        <template v-slot:item.1>
            <v-card title="Téléchargement du dataset" flat>
                <Form1 ref="form1" @form-validation="updateValidation" @uploaded="handleFileUpload"></Form1>
                <v-col cols="12">
                    <div class="text-end">
                        <v-btn color="primary" @click="validateStep(2)">Suivant</v-btn>
                    </div>
                </v-col>
            </v-card>
        </template>

        <template v-slot:item.2>
            <v-card title="Sélection des colonnes" flat>
                <Form2 ref="form2" @form-validation="updateValidation" :columns="columns" @selected="handleColumnsSelected"></Form2>
                <v-row cols="12" justify="space-between">
                    <v-col cols="auto">
                        <v-btn color="secondary" @click="previousStep(1)">Précédent</v-btn>
                    </v-col>
                    <v-col cols="auto">
                        <v-btn color="primary" @click="validateStep(3)">Suivant</v-btn>
                    </v-col>
                </v-row>
            </v-card>
        </template>

        <template v-slot:item.3>
            <v-card title="Visualisation" flat>
                <Form3 ref="form3" @form-validation="updateValidation" ></Form3>
                <v-col cols="12">
                    <div class="text-start">
                        <v-btn color="secondary" @click="previousStep(2)">Précédent</v-btn>
                    </div>
                </v-col>
            </v-card>
        </template>
    </v-stepper>
</template>
<script>
import Form1 from './Form1.vue';
import Form2 from './Form2.vue';
import Form3 from './Form3.vue';

export default {
    data() {
        return {
            activeStep: 1,
            columns: [], // Colonnes reçues après upload
        };
    },
    methods: {

        handleFileUpload(columns) {
            console.log("Received columns:", columns); // Vérifiez si cela est déclenché
            this.columns = columns; // Stockez les colonnes
        },



        async validateStep(nextStep) {
            let isValid = false;

            if (nextStep === 2 && this.$refs.form1) {
                isValid = await this.$refs.form1.validateForm();
            } else if (nextStep === 3 && this.$refs.form2) {
                isValid = await this.$refs.form2.validateForm();
                console.log(nextStep, isValid)
            }

            if (isValid) {
                this.activeStep = nextStep; // Change de step seulement si valide
            } else {
                console.log('Formulaire invalide, actions cachées.');
            }
        },

        async previousStep(nextStep) {
            this.activeStep = nextStep; // Change de step seulement si valide
        }
    }
}
</script>