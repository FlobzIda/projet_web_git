<template>
    <v-stepper
        v-model="activeStep"
        alt-labels
        hide-actions
        prev-text=""
        next-text=""
        :items="['Téléchargement du dataset', 'Sélection des colonnes', 'Visualisation', 'Liste des modèles']"
    >
        <template v-slot:item.1>
            <v-card title="Téléchargement du dataset" flat>
                <Form1 ref="form1" @uploaded="handleFileUpload" @form1ValidateEmit="form1ValideFonc" @fileName="fileNameEmit"></Form1>
                <v-row cols="12" justify="space-between">
                    <v-col cols="auto">
                        <v-btn color="secondary" @click="goToStep(4)">Voir tous les modèles</v-btn>
                    </v-col>
                    <v-col cols="auto">
                        <v-btn color="primary" @click="goToStep(2)" v-if="form1Valid">Configuer</v-btn>
                    </v-col>
                </v-row>
            </v-card>
        </template>

        <template v-slot:item.2>
            <v-card title="Sélection des colonnes" flat>
                <Form2 ref="form2" :fileName="fileName" :columnsForm2="columns" :preview="preview" @selected="handleColumnsSelected" @form2ValidateEmit="form2ValideFonc"></Form2>
                <v-row cols="12" justify="space-between">
                    <v-col cols="auto">
                        <v-btn color="secondary" @click="goToStep(1)">Précédent</v-btn>
                    </v-col>
                    <v-col cols="auto">
                        <v-btn color="primary" @click="goToStep(3); submitForm()" v-if="form2Valid">Tester</v-btn>
                    </v-col>
                </v-row>
            </v-card>
        </template>

        <template v-slot:item.3>
            <v-card title="Visualisation" flat>
                <Form3 ref="form3" :visuel="resultat"></Form3>
                <v-row cols="12"  justify="space-between">
                    <v-col cols="auto">
                        <v-btn color="secondary" @click="goToStep(2)">Précédent</v-btn>
                    </v-col>
                    <v-col cols="auto">
                        <v-btn color="primary" @click="enregistrementModel()">Enregistrer</v-btn>
                    </v-col>
                </v-row>
            </v-card>
        </template>

        <template v-slot:item.4>
            <v-card title="Enregistrement" flat>
                <Form4 ref="form3"></Form4>
                <v-row cols="12"  justify="space-between">
                    <v-col cols="auto">
                        <v-btn color="secondary" @click="goToStep(3)">Précédent</v-btn>
                    </v-col>
                    <v-col cols="auto">
                        <v-btn color="primary" @click="goToStep(1)">Nouveau Modèle</v-btn>
                    </v-col>
                </v-row>
            </v-card>
        </template>
    </v-stepper>
</template>

<script>
import Form1 from './Form1.vue';
import Form2 from './Form2.vue';
import Form3 from './Form3.vue';
import Form4 from './Form4.vue';

export default {
    data() {
        return {
            activeStep: 1,      // numéro de page du stepper
            columns: [],        // noms des colonnes
            colX: [],           // colonnes d'entrainement
            colY: [],           // colonne target
            preview: [],        // visuel du tableau
            form1Valid: false,  // formulaire 1 valide
            form2Valid: false,  // formulaire 2 valide
            fileName: "",       // nom du fichier
            resultat: {},        // resultat du l'entrainement
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
        async goToStep(nextStep) {
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
                    this.resultat = await response.json();
                    console.log("Model Trained successfully:", data);
                } else {
                    console.error("HTTP Error:", response.status);
                }
            } catch (error) {
                console.error("model trained failed:", error);
            }
        },

        enregistrementModel() {
            // Envoi des données du modèle au backend pour l'enregistrement
            const modelData = {
                colX: this.colX,
                colY: this.colY,
                fileName: this.fileName,
                resultat: this.resultat
            };

            fetch('/api/saveModel', {
                method: 'POST',
                body: JSON.stringify(modelData),
                headers: {
                'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log('Model saved successfully', data);
                this.goToStep(4); 
                // Vous pouvez ajouter des actions comme afficher un message de succès
            })
            .catch(error => {
                console.error('Error while saving model:', error);
            });
        }
    },
    components: {Form1, Form2, Form3}
}
</script>
