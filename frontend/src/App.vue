<template>

  <Stepper />

</template>

<script>
import Stepper from "./components/Stepper.vue";

export default {
  data() {
    return {
      step: 1, // Étape actuelle du stepper
      columns: [], // Colonnes reçues après upload
      selectedColumnsX: [], // Colonnes sélectionnées
      selectedColumnsY: [], // Colonnes sélectionnées
      accuracy: null, // Résultat du modèle
    };
  },
  methods: {
    handleFileUpload(columns) {
      console.log("Received columns:", columns); // Vérifiez si cela est déclenché
      this.columns = columns; // Stockez les colonnes
    },
    handleColumnsSelected(selectedColumnsX, selectedColumnsY) {
      this.selectedColumnsX = selectedColumnsX; // Stockez les colonnes sélectionnées
      this.selectedColumnsY = selectedColumnsY; // Stockez les colonnes sélectionnées
    },
    goToStep(stepNumber) {
      this.step = stepNumber; // Change l'étape actuelle
    },
    async trainModel() {
      try {
        const response = await fetch("http://127.0.0.1:5000/train", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            columnsX: this.selectedColumnsX,
            columnsY: this.selectedColumnsY
          }),
        });

        const data = await response.json();
        this.accuracy = data.accuracy;
      } catch (error) {
        console.error("Training failed:", error);
      }
    },
  },
  components: {Stepper},
};
</script>