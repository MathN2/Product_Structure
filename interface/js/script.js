
document.addEventListener("DOMContentLoaded", function () {

    const modalElemento = document.getElementById("modalEditar");
    const modal = bootstrap.Modal.getOrCreateInstance(modalElemento);

    const formulario = document.getElementById("formEditar");

    // Abre o modal e preenche os campos
    document.querySelectorAll(".btn-editar").forEach(function (botao) {

        botao.addEventListener("click", function () {

            const nome = botao.dataset.nome;
            const quantidade = botao.dataset.quantidade;
            const preco = botao.dataset.preco;

            document.getElementById("editarNome").value = nome;
            document.getElementById("editarQuantidade").value = quantidade;
            document.getElementById("editarPreco").value = preco;

            modal.show();
        });

    });

    // Captura o envio do formulário
    formulario.addEventListener("submit", function (event) {

        event.preventDefault();

        const dados = {
            nome: document.getElementById("editarNome").value,
            quantidade: document.getElementById("editarQuantidade").value,
            preco: document.getElementById("editarPreco").value
        };

        console.log("Dados para edição:", dados);

        alert("Dados preparados para edição!");

        modal.hide();
    });

});
