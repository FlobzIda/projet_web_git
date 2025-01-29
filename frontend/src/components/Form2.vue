<template>
    <v-form v-model="isValid" ref="form2">
        <v-container>
            <v-row>
                <v-col cols="12" md="6">
                    <v-select multiple clearable :items="columns" 
                        label="Sélectionner les colonnes X"
                        v-model="selectedColumnsX"
                        :rules="[rules.required]">
                    </v-select>
                </v-col>
                <v-col cols="12" md="6">
                    <v-select clearable :items="columns" 
                        label="Sélectionner la colonne Y" 
                        v-model="selectedColumnsY"
                        :rules="[rules.required]">
                    </v-select>
                </v-col>    
            </v-row>
            
            <v-btn @click="submitSelection">Confirm Selection</v-btn>
        </v-container>
    </v-form>
  </template>
  
  <script>
  export default {
    props: ["columns"],
    data() {
        return {
            isValid: false,
            selectedColumnsX: [],
            selectedColumnsY: [],
            rules: {
                required: (value) => !!value || 'Ce champ est requis',
            }
        };
    },
    watch: {
        isValid(newValue) {
            this.$emit('form-validation', newValue); // Envoie l'état de validation au parent
        }
    },
    methods: {
        submitSelection() {
            this.$emit("selectedX", this.selectedColumnsX);
            this.$emit("selectedY", this.selectedColumnsY);
        },
        async validateForm() {
            const validation = await this.$refs.form2.validate();
            return validation.valid;
        }
    }
  }
  </script>