export function axiosConfig(formdata = false) {
    return {
        headers: {
            "Content-Type": formdata ? "multipart/form-data" : "application/json",
        },
    };
}
