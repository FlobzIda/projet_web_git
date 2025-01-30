<template>
    <v-form v-model="isValid" ref="form">
        <v-container>
            <v-row>
                <v-col cols="12" md="6">
                    <v-select multiple clearable :items="columnsForm2"
                        label="Sélectionner les colonnes X"
                        v-model="selectedColumnsX"
                        @update:modelValue="handleInput1Change"
                        :rules="[rules.required]">
                    </v-select>
                </v-col>
                <v-col cols="12" md="6">
                    <v-select clearable :items="columnsForm2"
                        label="Sélectionner la colonne Y"
                        v-model="selectedColumnsY"
                        @update:modelValue="handleInput2Change"
                        :rules="[rules.required]">
                    </v-select>
                </v-col>
            </v-row>
            <v-row class="mb-10">
                <v-col cols="12">
                    <div class="text-center" >
                        <v-btn @click="displayPreviewFunc">{{ displayPreviewTxt }}</v-btn>
                    </div>
                </v-col>
                <v-col cols="12" v-if="displayPreview">
                    <v-data-table :headers="previewHeaders" :items="preview" item-value="name" class="elevation-1"></v-data-table>
                </v-col>
            </v-row>
            <div class="text-center" >
                <v-btn @click="submitSelection" items="fileName">Confirm Selection</v-btn>
            </div>
            
            <div class="text-center" >
                <p class="text-error">{{ this.errorForm2Txt }}</p>
            </div>
        </v-container>
    </v-form>
</template>

<script>
export default {
    props: ["columnsForm2", "preview", "fileName"],
    data() {
        return {
            isValid: false,
            selectedColumnsX: [],
            selectedColumnsY: [],
            errorForm2Txt: "",
            displayPreview: false,
            displayPreviewTxt: "Afficher la preview",
            rules: {
                required: (value) => !!value || 'Ce champ est requis',
            }
        };
    },
    computed: {
        previewHeaders() {
            return this.preview.length > 0 ? Object.keys(this.preview[0]).map(key => ({ text: key, value: key })) : [];
        }
    },
    methods: {
        submitSelection(items) {
            this.$emit("selected", this.selectedColumnsX, this.selectedColumnsY,this.fileName);
        },

        // Changement des valeurs des selects
        handleInput1Change(event) {
            console.log("handleInput1Change()")
            this.selectedColumnsX = event;
            this.validateForm();
        },
        handleInput2Change(event) {
            console.log("handleInput2Change()")
            this.selectedColumnsY = event;
            this.validateForm();
        },
        async validateForm() {
            console.log("validateForm()")

            const valid = this.selectedColumnsX.length > 0 && this.selectedColumnsY.length > 0;
            this.$emit("form2ValidateEmit", valid);
        },

        // Affiche ou chache la preview
        displayPreviewFunc() {
            if(this.displayPreview)
                this.displayPreviewTxt = "Afficher la preview";
            else
                this.displayPreviewTxt = "Cacher la preview";
            
            this.displayPreview = !this.displayPreview;
        }
    }
}
</script>