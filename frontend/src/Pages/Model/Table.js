import React, { useState } from "react";
import "./Table.css";
function Table({
  dcolumns,
  dvalues,
  colStatus,
  setcolStatus,
  rowStatus,
  setrowStatus,
}) {
  const handleOnChange = (type, position) => {
    let checkedState = [];
    if (type == "col") {
      checkedState = colStatus;
      const updatedCheckedState = checkedState.map((item, index) =>
        index == position ? !item : item
      );
      console.log(updatedCheckedState);
      setcolStatus(updatedCheckedState);
    } else {
      checkedState = rowStatus;
      const updatedCheckedState = checkedState.map((item, index) =>
        index == position ? !item : item
      );
      console.log(updatedCheckedState);
      setrowStatus(updatedCheckedState);
    }
  };
  return (
    <div>
      <table>
        <tr>
          {dcolumns.map((val, idx) => {
            return (
              <th>
                <span style={{ margin: "10px" }}>
                  <input
                    type="checkbox"
                    id={idx}
                    name="cols"
                    value={val}
                    checked={colStatus[idx]}
                    onChange={(e) => {
                      handleOnChange("col", e.target.id);
                    }}
                  />
                </span>

                {val}
              </th>
            );
          })}
        </tr>
        {dvalues.map((row, idx) => {
          return (
            <tr>
              {row.map((val, iidx) => {
                if (iidx == 0) {
                  return (
                    <td>
                      <span style={{ margin: "10px" }}>
                        <input
                          type="checkbox"
                          id={idx}
                          name="rows"
                          checked={rowStatus[idx]}
                          onChange={(e) => {
                            handleOnChange("row", e.target.id);
                          }}
                        />
                      </span>

                      {val}
                    </td>
                  );
                } else {
                  return <td>{val}</td>;
                }
              })}
            </tr>
          );
        })}
      </table>
    </div>
  );
}

export default Table;
