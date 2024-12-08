import React, {useState} from 'react';

export default function ComboBox() {
    // Define the model (array of objects with 'id' and 'name' properties)
    const model = [
        {id: 1, name: 'OpenAI'},
        {id: 2, name: 'Local llm'},
    ];

    // State to store the selected value
    const [selectedOption, setSelectedOption] = useState("1");

    // Handle the change in selection
    const handleSelectChange = (event) => {
        setSelectedOption(event.target.value);
    };

    return (
        <div className={"col-4"}>
            <label htmlFor="comboBox" style={{ fontSize: "large"}}>Model: </label>
            <select
                className={"w-200px m-2"}
                id="comboBox"
                value={selectedOption}
                onChange={handleSelectChange}
            >
                <option value="">-- Select an Option --</option>
                {model.map(option => (
                    <option key={option.id} value={option.id}>
                        {option.name}
                    </option>
                ))}
            </select>
        </div>
    );
};
