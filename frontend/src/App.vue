<template>

  <Stepper2/>

  <!--
  <v-stepper v-model="step">
    <v-stepper-content step="1">
      <StepOne @uploaded="handleFileUpload" />
      <v-btn @click="goToStep(2)" :disabled="columns.length === 0">Next</v-btn>
    </v-stepper-content>

    <v-stepper-content step="2">
      <StepTwo :columns="columns" @selected="handleColumnsSelected" />
      <v-btn @click="goToStep(3)"
        :disabled="columns.length === 0 || (selectedColumnsX.length === 0 && selectedColumnsY.length === 0)">Next</v-btn>
    </v-stepper-content>

    <v-stepper-content step="3">
      <StepThree :accuracy="accuracy" @train="trainModel" />
    </v-stepper-content>
  </v-stepper>-->
</template>

<script>
import StepOne from "./components/StepOne.vue";
import StepTwo from "./components/StepTwo.vue";
import StepThree from "./components/StepThree.vue";


import Stepper2 from "./components/Stepper2.vue";

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
  components: { StepOne, StepTwo, StepThree },
};
</script>