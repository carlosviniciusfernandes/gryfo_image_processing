const API_URL = 'http://localhost:8000/image/transform'

async function handleSubmit(event){
    event.preventDefault();

    const image = imgInput.files[0];
    const operations = []
    operationsMap.forEach((value, key, _) => {
        if (value) { operations.push(key); }
    })

    const formData = new FormData();
    formData.append('image', image);
    formData.append('operations', operations);

    const response = await fetch(API_URL, {
        method: 'post',
        body: formData,
        headers: {'Access-Control-Allow-Origin': '*'},
    }).catch((error) => ('Something went wrong!', error));

    const content = await response.blob();
    var img = URL.createObjectURL(content);
    imgTransformed.innerHTML = '<img src="' + img + '" class="img-cls" />';
};

const form = document.getElementById('form');
const imgInput = document.getElementById('img-input');
const imgPreview = document.getElementById('img-preview');
const imgTransformed = document.getElementById('img-transformed');
const imgOptions = document.getElementById('img-options');
const operationsMap = new Map(Object.entries({
    flip_horizontal: false,
    flip_vertical: false,
    invert_colors: false,
    blur: false,
    edge_detect: false,
    draw_contours: false,
}));

function loadImgPreview() {
    const files = imgInput.files[0];
    if (files) {
        const fileReader = new FileReader();
        fileReader.readAsDataURL(files);
        fileReader.addEventListener('load', function () {
            imgPreview.innerHTML = '<img src="' + this.result + '" class="img-cls"/>';
            imgTransformed.innerHTML = ''
        });
    }
}

imgInput.addEventListener('change', function () {
    loadImgPreview();
});
imgOptions.childNodes.forEach(item=>{
    if (item.tagName == 'INPUT') {
        item.addEventListener('change', function(e) {
            operationsMap.set(e.target.value, e.target.checked)
        })
    }
})
form.addEventListener('submit', handleSubmit);
