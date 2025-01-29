<template>
    <v-select multiple clearable :items="columns" label="Sélectionner les colonnes X"
        v-model="selectedColumnsX"></v-select>

    <v-select clearable :items="columns" label="Sélectionner la colonne Y" v-model="selectedColumnsY"></v-select>

    <v-btn @click="submitSelection">Confirm Selection</v-btn>
</template>

<script>
export default {
    props: ["columns"],
    data: () => ({
        selectedColumnsX: [],
        selectedColumnsY: [],
    }),
    methods: {
        submitSelection() {
            this.$emit("selectedX", this.selectedColumnsX);
            this.$emit("selectedY", this.selectedColumnsY);
        },
    },
};
</script>