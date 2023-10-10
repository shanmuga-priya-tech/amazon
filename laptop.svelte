<script>
    import { onMount } from "svelte"
    let product = []; 
    
    onMount(async()=>{
        let response=await fetch ("http://127.0.0.1:5000/amazon/laptops")
        let data= await response.json()
        product= data.products;
        console.log(product)
    })

  let currentPage = 0;

  function setCurrentPage(page) {
    currentPage = page;
  }

    
  </script>
  
  <h1>Laptops</h1>
  
  {#if product.length > 0}
    <table>
      <thead>
        <tr>
          <th>Product Name</th>
          <th>Product Image</th>
          <th>Original Price</th>
          <th>Current Price</th>
          <th>Star Rating</th>
        </tr>
      </thead>
      <tbody>
        {#each product as products, index}
        {#if index >= currentPage * 10 && index < (currentPage + 1) * 10}
          <tr>
            <td>{products.Product_name}</td>
            <td><img class="pic" src=" {products.img_url}" alt="laptop image" /></td>
            <td>{products.Original_price}</td>
            <td>{products.Current_price}</td>
            <td>{products.Star_rating}</td>
            
          </tr>
          {/if}
        {/each}
      </tbody>
    </table>
      <div class="pagination">
        {#each [...Array(Math.ceil(product.length / 10)).keys()] as page}
          <button on:click={() => setCurrentPage(page)}>{page + 1}</button>
        {/each}
      </div>
   
  {:else}
    <p>No products found.</p>
  {/if}

<style>
    table {
    border-collapse: collapse;
    width: 100%;
  }

   table, th, td {
    border: 1px solid #000; }

  th, td {
    padding: 10px;
  }
 th{
    font-size:22px;
 }
  th:nth-child(1), td:nth-child(1) {
    width: 30%; 
  } 
  .pic{
    max-height:100px;
  }
</style>


  