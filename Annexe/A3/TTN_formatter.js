function decodeUplink(input) {
    return {
        data : {
            temp: String.fromCharCode.apply(null, input.bytes)
        },
        warnings: [],
        errors: []
    };
}