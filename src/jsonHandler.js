const fs = require('fs');
const path = require('path');

// Função para ler os resultados do arquivo JSON (merge_results.json)
function readResults() {
    const filePath = path.join(__dirname, 'merged_results.json');  // Caminho para o arquivo de resultados

    if (!fs.existsSync(filePath)) {
        throw new Error('merged_results.json não encontrado.');
    }

    const data = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(data);  // Retorna os resultados como um objeto JavaScript
}

module.exports = {
    readResults
};
