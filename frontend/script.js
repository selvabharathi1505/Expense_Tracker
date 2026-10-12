const form = document.getElementById("expense-form");

form.addEventListener("submit", function(event) {
    event.preventDefault();

    const name = document.getElementById("name").value;
    const category = document.getElementById("category").value;
    const amount = Number(document.getElementById("amount").value);
    const date = document.getElementById("date").value;

    if (name.trim() === "" || category.trim() === "") {
        console.log("Name and category are required.");
        return;
    }

    if (amount <= 0 || !Number.isFinite(amount)) {
        console.log("Amount must be greater than zero.");
        return;
    }

    if (date === "") {
        console.log("Date is required.");
        return;
    }

    const expense = {
    name: name,
    category: category,
    amount: amount,
    date: date
};

    
const expenseJSON = JSON.stringify(expense);

fetch("http://127.0.0.1:8000/expenses", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: expenseJSON
})
.then(response => {
    if (!response.ok) {
        throw new Error("Failed to add expense");
    }

    return response.json();
})
.then(data => {
    
    console.log("Expense added successfully:", data);
    loadExpenses();
    loadSummary();})

.catch(error => {
    showServerError();
     console.error("Error Adding expense:", error);
});

});

//load expenses from backend and display in table

async function loadExpenses() {
    try {
        const response = await fetch("http://127.0.0.1:8000/expenses");

        if (!response.ok) {
            throw new Error("Failed to load expenses");
        }

        const expenses = await response.json();

        const expenseList = document.getElementById("expense-list");

        expenseList.innerHTML = "";

        expenses.forEach(function(expense) {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${expense.id}</td>
                <td>${expense.name}</td>
                <td>${expense.category}</td>
                <td>${expense.amount}</td>
                <td>${expense.date}</td>
                <td>
                    <button onclick="deleteExpense(${expense.id})">Delete</button>
                    <button onclick="editExpense(${expense.id})">Edit</button>
                </td>
            `;

            expenseList.appendChild(row);
        });
        
        console.log("Expenses displayed successfully");
    } catch (error) {
        showServerError();
         console.error("Error Loading expense:", error);
    }
}

loadExpenses();

//delete expense
async function deleteExpense(expenseId) {
    const confirmed = confirm("Are you sure you want to delete this expense?");

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(
            `http://127.0.0.1:8000/expenses/${expenseId}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            throw new Error("Failed to delete expense");
        }
        
        console.log("Expense deleted successfully");

        loadExpenses();
        loadSummary();
    } catch (error) {
         showServerError();
            console.error("Error Deleting expense:", error);
        
    }
}

//update expense


async function editExpense(expenseId) {
    try {
        const getResponse = await fetch(
            `http://127.0.0.1:8000/expenses/${expenseId}`
        );

        if (!getResponse.ok) {
            throw new Error("Failed to load expense");
        }

        const expense = await getResponse.json();

        const newName = prompt("Expense name:", expense.name);
        if (newName === null || newName.trim() === "") {
            return;
        }

        const newCategory = prompt("Category:", expense.category);
        if (newCategory === null || newCategory.trim() === "") {
            return;
        }

        const newAmount = prompt("Amount:", expense.amount);
        if (newAmount === null || newAmount.trim() === "") {
            return;
        }

        const newDate = prompt("Date (YYYY-MM-DD):", expense.date);
        if (newDate === null || newDate.trim() === "") {
            return;
        }

        const response = await fetch(
            `http://127.0.0.1:8000/expenses/${expenseId}`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: newName.trim(),
                    category: newCategory.trim(),
                    amount: Number(newAmount),
                    date: newDate
                })
            }
        );

        if (!response.ok) {
            throw new Error("Failed to update expense");
        }
        
        console.log("Expense updated successfully");
        loadExpenses();
        loadSummary();
    } catch (error) {
        showServerError();
            console.error("Error Updating expense:", error);
        
    }
}

//summary


async function loadSummary() {
    try {
        const response = await fetch("http://127.0.0.1:8000/summary");

        if (!response.ok) {
            throw new Error("Failed to load summary");
        }

        const summary = await response.json();
        

        document.getElementById("total-spending").textContent =
            summary.total_spending;

        const categorySummary = document.getElementById("category-summary");
        categorySummary.innerHTML = "";

        for (const category in summary.category_wise) {
            const item = document.createElement("li");

            item.textContent =
                `${category}: ₹${summary.category_wise[category]}`;

            categorySummary.appendChild(item);
        }
    } catch (error) {
        showServerError();
        console.error("Error Loading summary:", error);
    }
}

loadSummary();

//error message when FastAPI server is not running



function showError(message) {
    const errorContainer = document.getElementById("error-container");
    const errorMessage = document.getElementById("error-message");

    if (message === "") {
        errorContainer.hidden = true;
        return;
    }

    errorMessage.textContent = message;
    errorContainer.hidden = false;
}

function hideError() {
    document.getElementById("error-container").hidden = true;
}

function showServerError() {
    showError(
        "Unable to connect to the server. Please check your connection and try again."
    );
}

document.getElementById("retry-button").addEventListener("click", async () => {
    hideError();

    await Promise.all([
        loadExpenses(),
        loadSummary()
    ]);
});