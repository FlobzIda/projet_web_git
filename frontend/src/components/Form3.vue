<template>
    <div>
        <v-btn color="primary" @click="trainModel">Train Model</v-btn>
        <div v-if="accuracy !== null">
            <h3>Model Accuracy:</h3>
            <p>{{ accuracy }}</p>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        accuracy: {
            type: Number,
            default: null, // Définit une valeur par défaut pour éviter une erreur si la prop est absente
        },
    },
    methods: {
        trainModel() {
            this.$emit("train");
        },
    },
};
</script>