<template>
    <v-form v-model="isValid" ref="form1">
      <v-container>
        <v-row>
            <v-col cols="12">
                <v-file-input label="Upload CSV" accept=".csv" @change="handleFileChange"></v-file-input>
            </v-col>
        </v-row>
      </v-container>
    </v-form>
  </template>

<script>
export default {
  data() {
      return {
          isValid: false,
          file: null,
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
    handleFileChange(event) {
        this.file = event.target.files[0];
        console.log("Selected file:", this.file);
        this.uploadFile();
    },
    async uploadFile() {
        if (!this.file) {
            console.error("No file selected");
            return;
        }

        const formData = new FormData();
        formData.append("file", this.file);

        try {
            const response = await fetch("http://127.0.0.1:5000/upload", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error("File upload failed:", errorData);
                return;
            }

            const data = await response.json();
            console.log("File uploaded successfully:", data);
            this.$emit("uploaded", data.columns);
        } catch (error) {
            console.error("File upload failed:", error);
        }
    },

    async validateForm() {
        const validation = await this.$refs.form1.validate();
        return validation.valid;
    },
  }
}
</script>