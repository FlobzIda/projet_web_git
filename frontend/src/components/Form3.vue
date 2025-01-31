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
                <p>max_depth : {{ visuel.max_depth }}</p>
                <p>learning_rate: {{ visuel.learning_rate }}</p>
                <p>testSize : {{ visuel.testSize }}</p>
                <p>randomState : {{ visuel.randomState }}</p>
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
    },
};
</script>
