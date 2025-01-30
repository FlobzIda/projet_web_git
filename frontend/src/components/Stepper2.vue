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
                <Form1 ref="form1" @uploaded="handleFileUpload" @form1ValidateEmit="form1ValideFonc"></Form1>
                <v-col cols="12">
                    <div class="text-end">
                        <v-btn color="primary" @click="validateStep(2)" v-if="form1Valid">Suivant</v-btn>
                    </div>
                </v-col>
            </v-card>
        </template>

        <template v-slot:item.2>
            <v-card title="Sélection des colonnes" flat>
                <Form2 ref="form2" :columns="columns" :preview="preview" @selected="handleColumnsSelected" @form2ValidateEmit="form2ValideFonc"></Form2>
                <v-row cols="12" justify="space-between">
                    <v-col cols="auto">
                        <v-btn color="secondary" @click="previousStep(1)">Précédent</v-btn>
                    </v-col>
                    <v-col cols="auto">
                        <v-btn color="primary" @click="validateStep(3)" v-if="form2Valid">Suivant</v-btn>
                    </v-col>
                </v-row>
            </v-card>
        </template>

        <template v-slot:item.3>
            <v-card title="Visualisation" flat>
                <Form3 ref="form3"></Form3>
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
            columns: [],
            preview: [],
            form1Valid: false,
            form2Valid: false,
        };
    },
    methods: {
        handleFileUpload(data) {
            this.columns = data.columns;
            this.preview = data.preview;
        },
        async handleColumnsSelected(columnsX, columnY) {
            try {
                const response = await fetch("http://127.0.0.1:5000/select_columns", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ columnsX: columnsX, columnY: columnY })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    console.error("Column selection failed:", errorData);
                    return;
                }

                const data = await response.json();
                console.log("Columns selected successfully:", data);
            } catch (error) {
                console.error("Column selection failed:", error);
            }
        },
        async validateStep(nextStep) {
            
            this.activeStep = nextStep;

            // let isValid = false;

            // if (nextStep === 2 && this.$refs.form1) {
            //     isValid = await this.$refs.form1.validateForm();
            //     console.log("form1Valid", isValid)
            //     this.form1Valid = isValid;
            // } else if (nextStep === 3 && this.$refs.form2) {
            //     isValid = await this.$refs.form2.validateForm();
            //     console.log("form2Valid", isValid)
            //     this.form2Valid = isValid;
            // }

            // if (isValid) {
            //     console.log('Form valide')
            //     this.activeStep = nextStep;
            // } else {
            //     console.log('Formulaire invalide, actions cachées.');
            // }
        },
        async previousStep(nextStep) {
            this.activeStep = nextStep;
        },
        
        form1ValideFonc(isValidForm) {
            this.form1Valid = isValidForm
            console.log("form1ValideFonc", this.form1Valid)
        },

        form2ValideFonc(isValidForm) {
            this.form2Valid = isValidForm
            console.log("form2ValideFonc", this.form2Valid)
        }
    }
}
</script>
