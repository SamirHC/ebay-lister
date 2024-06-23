import React, { useState } from 'react';

const CreateInventoryItemPage = () => {
  const [message, setMessage] = useState('');

  const createItem = () => {
    fetch('/create_or_replace_inventory_item',
      {method: 'PUT'}
    )
      .then(response => response.json())
      .then(data => setMessage('Inventory item created or replaced successfully!'))
      .catch(error => setMessage('Error: ' + error.toString()));
  };

  return (
    <div>
      <button onClick={createItem}>Create or Replace Inventory Item</button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default CreateInventoryItemPage;