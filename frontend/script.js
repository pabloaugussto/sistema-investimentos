// URL da nossa API (garanta que a porta está correta e o backend rodando)
const apiUrl = 'http://127.0.0.1:8000/api/v1/investimentos/';

// Pega a referência do corpo da tabela no HTML
const tableBody = document.querySelector('#investments-table tbody');

/**
 * Formata a data (se necessário) para exibição.
 * @param {string} dataString - A data vinda da API.
 * @returns {string} - A data no formato AAAA-MM-DD.
 */
function formatarDataParaExibicao(dataString) {
    if (!dataString) return '';
    // Pega apenas a parte da data (antes do 'T', se houver)
    return dataString.split('T')[0];
}

/**
 * Busca todos os investimentos na API e preenche a tabela.
 */
async function carregarInvestimentos() {
    console.log("Iniciando busca de investimentos na API..."); // Mensagem para debug

    // Limpa a tabela e mostra 'Carregando...'
    tableBody.innerHTML = '<tr><td colspan="6" style="text-align: center;">Carregando...</td></tr>';

    try {
        // Faz a requisição GET para a API
        const response = await fetch(apiUrl);

        // Verifica se a requisição foi bem-sucedida (status 200-299)
        if (!response.ok) {
            throw new Error(`Erro na API! Status: ${response.status} - ${response.statusText}`);
        }

        // Converte a resposta para JSON
        const investimentos = await response.json();
        console.log("Dados recebidos:", investimentos); // Mensagem para debug

        // Limpa a tabela novamente antes de adicionar os dados
        tableBody.innerHTML = '';

        // Verifica se há investimentos para exibir
        if (investimentos.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="6" style="text-align: center;">Nenhum investimento cadastrado.</td></tr>';
            return;
        }

        // Itera sobre cada investimento e cria uma linha na tabela
        investimentos.forEach(inv => {
            const tr = document.createElement('tr'); // Cria uma nova linha <tr>
            tr.innerHTML = `
                <td>${inv.id}</td>
                <td>${inv.nome}</td>
                <td>${inv.tipo}</td>
                <td>R$ ${inv.valor.toFixed(2)}</td>
                <td>${formatarDataParaExibicao(inv.data_investimento)}</td>
                <td>
                    <button class="btn-edit" data-id="${inv.id}">Editar</button>
                    <button class="btn-delete" data-id="${inv.id}">Excluir</button>
                </td>
            `;
            tableBody.appendChild(tr); // Adiciona a linha ao corpo da tabela
        });

    } catch (error) {
        console.error("Erro ao carregar investimentos:", error);
        // Exibe uma mensagem de erro na tabela
        tableBody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: red;">Falha ao carregar. Verifique o console (F12) e se o backend está rodando com CORS.</td></tr>`;
        alert("Falha ao carregar os dados da API. Verifique o console (F12).");
    }
}

// Adiciona um "ouvinte de evento" que chama a função 'carregarInvestimentos'
// assim que todo o conteúdo HTML da página for carregado.
document.addEventListener('DOMContentLoaded', carregarInvestimentos);