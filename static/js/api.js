//
// Camada de integração do Frontend com a API (fetch)
// Cada função abaixo trata um fluxo (criar, visualizar, atualizar, deletar)
// e exibe mensagens amigáveis ao usuário.
//

// Função para criar novo paciente
async function createPatient(event) {
    event.preventDefault();
    
    // Coleta dados do formulário (IDs seguem o HTML dos templates)
    const formData = {
        name: document.getElementById('nome').value,
        birth_date: document.getElementById('data_nascimento').value,
        gender: document.getElementById('genero').value,
        height: document.getElementById('altura').value,
        weight: document.getElementById('peso').value
    };
    
    try {
        // Envia requisição POST para criar paciente
        const response = await fetch('/api/paciente/criar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Paciente cadastrado com sucesso!');
            document.querySelector('form').reset();
            setTimeout(() => {
                window.location.href = '/listar';
            }, 1000);
        } else {
            alert('Erro: ' + result.error);
        }
    } catch (error) {
        alert('Erro ao cadastrar: ' + error.message);
    }
}

async function viewPatient(patientId) {
    try {
        // Busca dados do paciente pelo ID
        const response = await fetch('/api/paciente/' + patientId);
        const result = await response.json();
        
        if (result.success) {
            const patient = result.patient;
            // Monta mensagem com dados básicos e cálculos derivados
            const message = 'ID: ' + patient.id + '\n' +
                'Nome: ' + patient.name + '\n' +
                'Altura: ' + patient.height + 'm\n' +
                'Peso: ' + patient.weight + 'kg\n' +
                'Genero: ' + (patient.biological_gender === 'M' ? 'Masculino' : 'Feminino') + '\n' +
                'Idade: ' + result.age + ' anos\n' +
                'IMC: ' + result.bmi + ' (' + result.bmi_classification + ')\n' +
                'Taxa Metabolica Basal: ' + result.basal_metabolic_rate + ' kcal/dia';
            alert(message);
        } else {
            alert('Paciente nao encontrado');
        }
    } catch (error) {
        alert('Erro ao buscar paciente: ' + error.message);
    }
}
 
// Função para redirecionar para página de visualizar (botão 'Ver' na lista)
function goToViewPatient(patientId) {
    window.location.href = '/visualizar?id=' + patientId;
}

async function deletePatient(event) {
    event.preventDefault();
    
    const patientId = document.getElementById('id_paciente').value;
    
    // Busca dados do paciente primeiro para exibir o nome na confirmação
    try {
        const getResponse = await fetch('/api/paciente/' + patientId);
        const getData = await getResponse.json();
        
        if (!getData.success) {
            alert('Paciente não encontrado');
            return;
        }
        
        const patientName = getData.patient.name;
        
        if (!confirm('Tem certeza que deseja deletar o paciente "' + patientName + '"?')) {
            return;
        }
        
        // Confirmação aceita: envia requisição de deleção
        const response = await fetch('/api/paciente/' + patientId + '/deletar', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Paciente deletado com sucesso!');
            document.querySelector('form').reset();
            setTimeout(() => {
                window.location.href = '/listar';
            }, 1000);
        } else {
            alert('Erro: ' + result.error);
        }
    } catch (error) {
        alert('Erro ao deletar: ' + error.message);
    }
}

async function updatePatient(event) {
    event.preventDefault();
    
    const patientId = document.getElementById('id_paciente').value;
    
    // Monta payload apenas com campos preenchidos para atualização parcial (PATCH-like)
    const formData = {
        name: document.getElementById('nome').value || null,
        height: document.getElementById('altura').value || null,
        weight: document.getElementById('peso').value || null,
        gender: document.getElementById('sexo').value || null
    };
    
    Object.keys(formData).forEach(key => formData[key] === null && delete formData[key]);
    
    if (Object.keys(formData).length === 0) {
        alert('Preencha pelo menos um campo para atualizar');
        return;
    }
    
    try {
        // Envia atualização via PUT
        const response = await fetch('/api/paciente/' + patientId + '/atualizar', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Paciente atualizado com sucesso!');
            document.querySelector('form').reset();
            setTimeout(() => {
                window.location.href = '/listar';
            }, 1000);
        } else {
            alert('Erro: ' + result.error);
        }
    } catch (error) {
        alert('Erro ao atualizar: ' + error.message);
    }
}

async function searchPatient(event) {
    event.preventDefault();
    
    const patientId = document.getElementById('id_paciente').value;
    
    if (!patientId) {
        alert('Digite um ID');
        return;
    }
    
    // Reutiliza a função de visualização para exibir informações
    await viewPatient(patientId);
}
