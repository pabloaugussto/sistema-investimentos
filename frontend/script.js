// URL da nossa API
const apiUrl = 'http://127.0.0.1:8000/api/v1/investimentos/';

// Elementos do DOM
const tableBody = document.querySelector('#investments-table tbody');
const investmentForm = document.getElementById('investment-form');
const investmentIdInput = document.getElementById('investment-id');
const nomeInput = document.getElementById('nome');
const tipoInput = document.getElementById('tipo');
const valorInput = document.getElementById('valor');
const dataInput = document.getElementById('data');
const btnSalvar = investmentForm.querySelector('button[type="submit"]');
const btnCancelar = document.getElementById('btn-cancelar');

/**
 * Formata a data para AAAA-MM-DD.
 */
function formatarDataParaInput(dataString) {
    if (!dataString) return '';
    return dataString.split('T')[0];
}

/**
 * Limpa o formulário e o reseta para o modo "Adicionar".
 */
function resetarFormulario() {
    investmentForm.reset(); // Limpa os campos
    investmentIdInput.value = ''; // Garante que o ID oculto está vazio
    btnSalvar.textContent = 'Salvar'; // Restaura o texto do botão
    btnCancelar.style.display = 'none'; // Esconde o botão Cancelar
    nomeInput.focus(); // Coloca o foco no primeiro campo
}

/**
 * Busca todos os investimentos na API e preenche a tabela.
 */
async function carregarInvestimentos() {
    tableBody.innerHTML = '<tr><td colspan="6" style="text-align: center;">Carregando...</td></tr>';
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) throw new Error(`Erro na API! Status: ${response.status}`);
        const investimentos = await response.json();
        tableBody.innerHTML = ''; // Limpa a tabela

        if (investimentos.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="6" style="text-align: center;">Nenhum investimento cadastrado.</td></tr>';
            return;
        }

        investimentos.forEach(inv => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${inv.id}</td>
                <td>${inv.nome}</td>
                <td>${inv.tipo}</td>
                <td>R$ ${inv.valor.toFixed(2)}</td>
                <td>${formatarDataParaInput(inv.data_investimento)}</td>
                <td>
                    <button class="btn-edit" data-id="${inv.id}">Editar</button>
                    <button class="btn-delete" data-id="${inv.id}">Excluir</button>
                </td>
            `;
            tableBody.appendChild(tr);
        });
    } catch (error) {
        console.error("Erro ao carregar investimentos:", error);
        tableBody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: red;">Falha ao carregar. Verifique o console (F12).</td></tr>`;
    }
}

/**
 * Preenche o formulário com dados de um investimento para edição.
 * @param {number} id - O ID do investimento a ser editado.
 */
async function preencherFormularioParaEditar(id) {
    console.log(`Buscando dados para editar ID: ${id}`);
    try {
        const response = await fetch(`${apiUrl}${id}`);
        if (!response.ok) throw new Error(`Erro ao buscar ID ${id}! Status: ${response.status}`);
        const inv = await response.json();

        investmentIdInput.value = inv.id;
        nomeInput.value = inv.nome;
        tipoInput.value = inv.tipo;
        valorInput.value = inv.valor;
        dataInput.value = formatarDataParaInput(inv.data_investimento);

        btnSalvar.textContent = 'Atualizar'; // Muda o texto do botão
        btnCancelar.style.display = 'inline-block'; // Mostra o botão Cancelar
        window.scrollTo(0, 0); // Rola para o topo (onde está o form)
        nomeInput.focus();

    } catch (error) {
        console.error("Erro ao preencher formulário:", error);
        alert("Não foi possível carregar os dados para edição.");
    }
}

/**
 * Salva (Adiciona ou Edita) um investimento.
 * @param {Event} event - O evento de submit.
 */
async function salvarInvestimento(event) {
    event.preventDefault();

    const id = investmentIdInput.value;
    const nome = nomeInput.value;
    const tipo = tipoInput.value;
    const valor = parseFloat(valorInput.value);
    const data = dataInput.value;

    const investimentoData = { nome, tipo, valor, data_investimento: data };

    let metodo = id ? 'PUT' : 'POST'; // Se tem ID, é PUT; senão, é POST
    let url = id ? `${apiUrl}${id}` : apiUrl;

    try {
        const response = await fetch(url, {
            method: metodo,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(investimentoData),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(`Erro ao salvar: ${response.statusText} - ${errorData.detail || 'Sem detalhes'}`);
        }

        alert(`Investimento ${id ? 'atualizado' : 'adicionado'} com sucesso!`);
        resetarFormulario();
        carregarInvestimentos();

    } catch (error) {
        console.error("Falha ao salvar:", error);
        alert(`Não foi possível salvar. Erro: ${error.message}`);
    }
}

/**
 * Exclui um investimento.
 * @param {number} id - O ID do investimento a ser excluído.
 */
async function excluirInvestimento(id) {
    if (!confirm(`Tem certeza que deseja excluir o investimento ID ${id}?`)) {
        return;
    }

    try {
        const response = await fetch(`${apiUrl}${id}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            throw new Error(`Erro ao excluir: ${response.statusText}`);
        }

        alert('Investimento excluído com sucesso!');
        carregarInvestimentos();

    } catch (error) {
        console.error("Falha ao excluir:", error);
        alert(`Não foi possível excluir. Erro: ${error.message}`);
    }
}

// --- Event Listeners ---

// Carrega os dados quando a página carrega
document.addEventListener('DOMContentLoaded', carregarInvestimentos);

// Listener para o formulário (Adicionar/Atualizar)
investmentForm.addEventListener('submit', salvarInvestimento);

// Listener para o botão Cancelar Edição
btnCancelar.addEventListener('click', resetarFormulario);

// Listener na Tabela para os botões Editar e Excluir (Delegação)
tableBody.addEventListener('click', (event) => {
    const target = event.target; // Onde o clique ocorreu

    // Verifica se foi no botão Excluir
    if (target.classList.contains('btn-delete')) {
        const id = target.dataset.id; // Pega o ID do atributo 'data-id'
        excluirInvestimento(id);
    }

    // Verifica se foi no botão Editar
    if (target.classList.contains('btn-edit')) {
        const id = target.dataset.id; // Pega o ID do atributo 'data-id'
        preencherFormularioParaEditar(id);
    }
});