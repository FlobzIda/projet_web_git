<template>
    <v-form v-model="isValid" ref="form">
      <v-container>
        <v-row>
            <v-col cols="12">
                <v-file-input 
                    label="Upload CSV" 
                    accept=".csv"
                    @change="handleFileChange"
                    :rules="[rules.required]">
                </v-file-input>
            </v-col>
        </v-row>
        <div class="text-center" >
            <p class="text-error">{{ this.errorForm1Txt }}</p>
        </div>
      </v-container>
    </v-form>
</template>

<script>
export default {
  data() {
      return {
            isValid: false,
            file: null,
            errorForm1Txt: "",
            rules: {
                required: (value) => !!value || 'Ce champ est requis',
            }
      };
  },
  methods: {
    handleFileChange(event) {
        this.file = event.target.files[0];
        if(!this.file) {
            this.errorForm1Txt = "La saisie n'est pas bonne ou le format du fichier n'est pas un csv"
        }
        console.log("Un nouveau fichier est saisie.");
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
            console.log("a")
            const response = await fetch("/api/upload", {
                method: "POST",
                body: formData,
            });
            console.log("b: ", response)
            if (!response.ok) {
                const errorData = await response.json();
                console.error("File upload failed1:", errorData);
                console.log("c")
                return;
            }
            console.log("d")
            const data = await response.json();
            console.log("e")
            this.$emit("uploaded", data);
            this.$emit("form1ValidateEmit", true);
        } catch (error) {
            console.log("f")
            console.error("File upload failed2:", error);
        }
    },
}
}
</script>
