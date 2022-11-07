var test_url='http://important:10000'

describe('The Application', () => {
  it('is running.', () => {
    cy.visit(test_url)
  });
})