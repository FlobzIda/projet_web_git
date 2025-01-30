<template>
    <v-form v-model="isValid" ref="form">
      <v-container>
        <v-row>
            <v-col cols="12">
                <v-file-input clearable label="Upload CSV" 
                    accept=".csv"
                    @change="handleFileChange"
                    :rules="[rules.required]"></v-file-input>
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
  methods: {
    handleFileChange(event) {
        this.file = event.target.files[0];
        this.uploadFile();
    },
    async uploadFile() {
        if (!this.file) {
            console.error("No file selected");
            this.$emit("form1ValidateEmit", false);
            return;
        }

        const formData = new FormData();
        formData.append("file", this.file);

        try {
            const response = await fetch("/api/upload", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error("File upload failed:", errorData);
                return;
            }

            const data = await response.json();
            console.log(data)
            this.$emit("uploaded", data);
            this.$emit("form1ValidateEmit", true);
        } catch (error) {
            console.error("File upload failed:", error);
        }
    },
    async validateForm() {
        const { valid } = await this.$refs.form.validate();
        return valid && !!this.file; // Vérifie si le fichier est sélectionné
    }
}
}
</script>
