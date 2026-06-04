// Must start app container (see docker-compose.yml)
var test_url='http://127.0.0.1:10000'

describe('The Application', () => {
  it('is running.', () => {
    cy.visit(test_url)
  });
})