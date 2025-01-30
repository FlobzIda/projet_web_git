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
            <Form1 ref="form1" @uploaded="handleFileUpload" @form1ValidateEmit="form1ValideFonc" @fileName="fileNameEmit"></Form1>
                <v-col cols="12">
                    <div class="text-end">
                        <v-btn color="primary" @click="validateStep(2)" v-if="form1Valid">Suivant</v-btn>
                    </div>
                </v-col>
            </v-card>
        </template>

        <template v-slot:item.2>
            <v-card title="Sélection des colonnes" flat>
                <Form2 ref="form2" :fileName="fileName" :columnsForm2="columns" :preview="preview" @selected="handleColumnsSelected" @form2ValidateEmit="form2ValideFonc"></Form2>
                <v-row cols="12" justify="space-between">
                    <v-col cols="auto">
                        <v-btn color="secondary" @click="previousStep(1)">Précédent</v-btn>
                    </v-col>
                    <v-col cols="auto">
                        <v-btn color="primary" @click="validateStep(3); submitForm()" v-if="form2Valid">Suivant</v-btn>
                    </v-col>
                </v-row>
            </v-card>
        </template>

        <template v-slot:item.3>
            <v-card title="Visualisation" flat>
                <Form3 ref="form3" :visuel="dataViz"></Form3>
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
            colX: [],
            colY: [],
            preview: [],
            form1Valid: false,
            form2Valid: false,
            fileName: "",
            dataViz: "",
        };
    },
    methods: {
        handleFileUpload(data) {
            this.columns = data.columns;
            this.preview = data.preview;
            this.fileName = data.fileName;
        },
        async handleColumnsSelected(columnsX, columnY) {
            this.colX = columnsX;
            this.colY = columnY;
            try {
                const response = await fetch("/api/select_columns", {
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
                this.dataViz = data;
                console.log("Columns selected successfully:", data);
            } catch (error) {
                console.error("Column selection failed:", error);
            }
        },
        async validateStep(nextStep) {
            
            this.activeStep = nextStep;
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
        },

        fileNameEmit(isValidForm) {
            this.fileName = isValidForm
            console.log("fileNameEmit", this.fileName)
        },

        async submitForm() {
            try {
                const response = await fetch("/api/trainModel", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"  // Indique que le corps est en JSON
                    },
                    body: JSON.stringify({
                        filename: this.fileName,
                        colsX: this.colX,
                        colY: this.colY
                    })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    console.error("Error model :", errorData);
                    return;
                }

                if (response.ok) {
                    const data = await response.json();
                    console.log("Model Trained successfully:", data);
                } else {
                    console.error("HTTP Error:", response.status);
                }
            } catch (error) {
                console.error("model trained failed:", error);
            }
        }
    },
    components: {Form1, Form2, Form3}
}
</script>
