# escolaALF
Api para a escola ALF

## API 
 rodando na porta 5000
    
## URI de aluno
 controla chamadas para Aluno tipo GET, POST, PUT, DELETE
 
 GET: params -> id:? onde: 0  = todos order id, 
                           -1 = todos order nome
                           ? = valr numerico indicado o id desejado
                           
 POST: body -> JSON do aluno para Update no DB
               exemplo: { "id" : 1 , "nome" : "Marlon Spiess"}
               
 PUT: body -> JSON do aluno para Insert no DB
              exemplo: { "id" : 0 , "nome" : "Marlon Spiess"}
              retorno do ID gerado ou mesnsagem de erro
              
 DELETE: params -> id:? onde ? é o valor do id desejado p/ excluir 
     

    
## URI de prova
 controla chamadas para Aluno tipo GET, POST, PUT, DELETE
 
 GET: params -> id:? onde ? é o valor do id desejado
 
 POST: body -> (raw/json) JSON do aluno para Update no DB
               exemplo: { "id" : 1 , "nome" : "Python I"}
               
 PUT: body -> (raw/json) JSON do aluno para Insert no DB
              exemplo: { "id" : 0 , "nome" : "Python inciante"}
              retorno do ID gerado ou mesnsagem de erro
              
 DELETE: params -> id:? onde ? é o valor do id desejado p/ excluir 
    

    
## URI de resposta       
 controla chamadas para Aluno tipo PUT - exclusivamente para inclusão
 
 PUT: body -> JSON do aluno para Insert no DB
              exemplo: { ?????????????????????? }
              retorno do ID gerado ou mesnsagem de erro
    

