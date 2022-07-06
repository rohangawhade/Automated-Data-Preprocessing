import React from 'react'
import HomeCards from '../../Components/Cards/HomeCards';
import datapreprocess from '../../assets/datapreprocess.png';
import mod from '../../assets/mod.svg';
// import model from '../../assets/model.png';
import completeModel from '../../assets/completeModel.jpg';
import { useHistory } from 'react-router-dom';

import { useAuth } from '../../Components/Contexts/AuthContext';

export default function HomePage() {
    const { currentUser } = useAuth();
    const history = useHistory();
    // console.log(currentUser);
    if( !currentUser ){
        history.push("/signup");
    }
    const Features = 3;
    const titles = [
        "Data Preprocessing",
        "Build Model",
        "Complete ML"
    ];
    const descriptions = [
        "Preprocess your dataset in one step",
        "Pass Processed dataset and get your model at ease",
        "Build a model with complete ML steps"
    ];
    const images = [
        datapreprocess,
        mod,
        completeModel
    ]
    return (
        <div>
            <div style={{display: 'flex', flexWrap: 'wrap'}}>
                {
                    (() => {
                        const cards = [];
                        for(let i=0; i<Features; i++){
                            cards.push(<HomeCards key={i} title={titles[i]} description={descriptions[i]} imgSrc={images[i]} />);
                        }
                        return cards;
                    })()
                }
            </div>
        </div>
    )
}
