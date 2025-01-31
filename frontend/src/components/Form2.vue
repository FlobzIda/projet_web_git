<template>
    <v-form v-model="isValid" ref="form">
        <v-container>
            <v-row>
                <v-col cols="12" md="6">
                    <v-select
                        multiple
                        clearable
                        :items="availableColumnsX"
                        label="Sélectionner les colonnes X"
                        v-model="selectedColumnsX"
                        @update:modelValue="handleInput1Change"
                        :rules="[rules.required]">
                    </v-select>
                </v-col>
                <v-col cols="12" md="6">
                    <v-select
                        :items="availableColumnsY"
                        label="Sélectionner la colonne Y"
                        v-model="selectedColumnsY"
                        @update:modelValue="handleInput2Change"
                        :rules="[rules.required]">
                    </v-select>
                </v-col>
                <v-text-field
                    label="Saisir un randomState"
                    type="number"
                    v-model="randomState"
                    @update:modelValue="changementInputRANDOM"
                />
                <v-select
                label="Choisir un testSize"
                :items="[0.1, 0.15, 0.2, 0.25, 0.3]"
                v-model="testSize"
                @update:modelValue="changementInputTESTSIZE"
                />
                <v-select
                label="Choisir un learningRate"
                :items="[0.1, 0.01, 0.001, 0.0001, 0.00001, 0.00000000000001]"
                v-model="learningRate"
                @update:modelValue="changementInputLEARNING"
                />
                <v-text-field
                    label="Saisir un maxDepth"
                    type="number"
                    v-model="maxDepth"
                    @update:modelValue="changementInputMAXDEPTH"
                />
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
            randomState : 31,   //Random state défault = 31 RPZ a la vie a la mort
            testSize : 0.2,     //20 % de test size par défault
            learningRate : 0.01,//0.01 de learning rate de base
            maxDepth : 6,
            errorForm2Txt: "",
            displayPreview: false,
            displayPreviewTxt: "Afficher la preview",
            rules: {
                required: (value) => !!value || 'Ce champ est requis',
            }
        };
    },
    computed: {
        availableColumnsX() {
            return this.columnsForm2.filter(col => !this.selectedColumnsY.includes(col));
        },
        availableColumnsY() {
            return this.columnsForm2.filter(col => !this.selectedColumnsX.includes(col));
        },
        previewHeaders() {
            return this.preview.length > 0 ? Object.keys(this.preview[0]).map(key => ({ text: key, value: key })) : [];
        }
    },
    methods: {

        // Changement des valeurs des selects
        handleInput1Change(newValue) {
            //console.log("handleInput1Change()")
            this.selectedColumnsX = newValue;
            this.validateForm();
        },
        changementInputRANDOM(newValue) {
            //console.log("handleInput1Change()")
            this.randomState = newValue;
            console.log('jessaie de changer randomstate')
            console.log(this.randomState)
            this.validateForm();
        },
        changementInputTESTSIZE(newValue) {
            //console.log("handleInput1Change()")
            this.testSize = newValue;
            this.validateForm();
        },
        changementInputLEARNING(newValue) {
            //console.log("handleInput1Change()")
            this.learningRate = newValue;
            this.validateForm();
        },
        changementInputMAXDEPTH(newValue) {
            //console.log("handleInput1Change()")
            this.maxDepth = newValue;
            this.validateForm();
        },
        handleInput2Change(newValue) {
            //console.log("handleInput2Change()")
            this.selectedColumnsY = newValue;
            this.validateForm();
        },
        async validateForm() {
            console.log("validateForm()")
            let valid = this.selectedColumnsX.length > 0 && this.selectedColumnsY.length > 0;
            this.$emit("form2ValidateEmit", valid);
            if (valid)
                this.$emit("selected", this.selectedColumnsX, this.selectedColumnsY,this.randomState, this.testSize, this.learningRate, this.maxDepth);
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
