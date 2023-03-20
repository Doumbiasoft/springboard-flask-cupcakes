
const BASE_URL = "http://127.0.0.1:5000/api";

/** given data about a cupcake, generate html */

function generateMarkupHTML(cupcake) {
  return `
    <div data-cupcake-id="${cupcake.id}" class="col">
        <div class="card p-2 h-100">
            <img loading="lazy" class="card-img-top " alt="no image"  src="${cupcake.image}" />
            <div class="card-body">
                <p class="card-text"><b>Flavor:</b>&nbsp;${cupcake.flavor}</p>
                <p class="card-text"><b>Size:</b>&nbsp;<span class="text-success">${cupcake.size}</span></p>
                <p class="card-text"><b>Rating:</b>&nbsp;${cupcake.rating}&nbsp;<i class="fa fas fa-star text-warning"></i></p>
                <a class="btn btn-sm  btn-danger delete-cup" >Delete&nbsp;<i class="fas fa fas fa-trash-alt"></i></a>
            </div>
        </div>
    </div>
  `;
}

/** put initial cupcakes on page. */

async function InitialCupcakes() {
  const response = await axios.get(`${BASE_URL}/cupcakes`);

  for (let cupcakeData of response.data.cupcakes) {
    const $cupcake = $(generateMarkupHTML(cupcakeData));
    $("#card-cupcake").append($cupcake);
  }
}


/** handle form for adding of new cupcakes */

$("#form-new-cupcake").on("submit", async function (e) {
  e.preventDefault();

  const flavor = $("#flavor").val();
  const rating = $("#rating").val();
  const size = $("#size").val();
  const image = $("#image").val();

  const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image
  });

  const newCupcake = $(generateMarkupHTML(newCupcakeResponse.data.cupcake));
  $("#card-cupcake").append(newCupcake);
  $("#form-new-cupcake").trigger("reset");
});


/** handle clicking delete: delete cupcake */

$("#card-cupcake").on("click", ".delete-cup", async function (e) {
  e.preventDefault();
  const $cupcake = $(e.target).parent().parent().parent();
  const cupcakeId = $cupcake.attr("data-cupcake-id");
  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  $cupcake.remove();

});

$(InitialCupcakes);