<template>
    <v-row justify="center" v-if="models.length > 0">
        <v-col cols="auto" v-for="(model, index) in models" :key="index">
            <v-card class="mx-auto" width="300">
                 <v-img height="200px" cover
                 :src="'data:image/png;base64,' + model.resultat.learning_curve" alt="Learning Curve" >
                </v-img>
                <v-card-title>
                    Modèle : {{ index + 1 }}
                </v-card-title>

                <v-card-subtitle>
                    Accuracy : {{ model.resultat.accuracy }}
                </v-card-subtitle>

                <div class="pa-5">
                    <p>Colonnes X : {{ model.colX }}</p>
                    <p>Colonne Y : {{ model.colY }}</p>
                    <p>max_depth : {{ model.resultat.max_depth }}</p>
                    <p>learning_rate: {{ model.resultat.learning_rate }}</p>
                    <p>testSize : {{ model.resultat.testSize }}</p>
                    <p>randomState : {{ model.resultat.randomState }}</p>
                </div>
            </v-card>
        </v-col>
    </v-row>
    <div class="text-center" v-else>
        <p>Aucun modèle enregistré</p>
    </div>
</template>

<script>
export default {
    props: [],
    data() {
        return {
            models: []
        };
    },
    mounted() {
        // Appel pour récupérer les données des modèles
        this.fetchModels();
    },
    methods: {
        async fetchModels() {
            try {
                const response = await fetch('/api/getModels');  // Requête GET vers votre backend
                if (!response.ok) {
                    throw new Error('Erreur lors de la récupération des modèles');
                }
                
                const data = await response.json();  // Parse la réponse JSON
                if (data.status === 'success') {
                    this.models = data.models;  // Mettez à jour les données dans le state
                    // this.$emit("models", this.models)
                } else {
                    console.log('Aucun modèle trouvé');
                }
            } catch (error) {
                console.error('Erreur lors de la récupération des modèles:', error);
            }
        }
    },
};
</script>
