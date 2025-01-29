<template>
    <v-file-input label="Upload CSV" accept=".csv" @change="handleFileChange"></v-file-input>
</template>

<script>
export default {
    data() {
        return {
            file: null,
        };
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
    },
};
</script>