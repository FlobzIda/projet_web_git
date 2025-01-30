<template>
    <div>
        <!-- <v-btn color="primary" @click="trainModel">Train Model</v-btn>-->
        <div v-if="accuracy !== null">
            <div class="text-center mb5">
                <h3>Model Accuracy:</h3>
                <p>{{ visuel.accuracy }}</p>
            </div>
            <div class="text-start">
                <p>Colonne d'entrainement : {{ visuel.columns_x }}</p>
                <p>Colonne cible : {{ visuel.column_y }}</p>
            </div>
            <img :src="'data:image/png;base64,' + visuel.feature_importance" alt="Learning Curve" />
            <img :src="'data:image/png;base64,' + visuel.feature_importance" alt="Feature Importance" />
        </div>
    </div>
</template>

<script>
export default {
    props: ["visuel"],
    data() {
        return {
        };
    },
    methods: {
        async trainModel() {
            try {
                const response = await fetch("/api/trainModel", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ columns: this.selectedColumns })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    console.error("Model training failed:", errorData);
                    return;
                }

                const data = await response.json();
                this.accuracy = data.accuracy;
            } catch (error) {
                console.error("Model training failed:", error);
            }
        },
    },
};
</script>
