module Tags.View exposing (..)

import Types exposing (..)
import State exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput, onClick, onCheck)


view : Model -> Html Msg
view model =
    div [ class "overflow-hidden ph2 mt2" ]
        [ div [ class "tl w-60-ns center" ] [ h3 [] [ text "Personalise your results:" ] ]
        , div [ class ("tag-container w-200-ns w-330 relative center " ++ (getPosition model.tag_position)) ]
            [ render_filter_block model 1 model.issue_label model.issue_tags ("mr-1p-ns mr-5 " ++ (get_active model 1))
            , render_filter_block model 2 model.reason_label model.reason_tags ("mr-1p-ns mr-5 " ++ (get_active model 2))
            , render_filter_block model 3 model.content_label model.content_tags (get_active model 3)
            ]
        ]


render_filter_block : Model -> Int -> String -> List String -> String -> Html Msg
render_filter_block model num filter_label tags classname =
    div
        [ class
            ("tag-card br1 shadow-2 w-30 tl pa4-ns pa3 mb3 dib h6 v-mid relative "
                ++ classname
                ++ if not (is_active model num) then
                    " pointer"
                   else
                    ""
            )
        , onClick
            (if (is_active model num) then
                NoOp
             else
                (ChangePosition num)
            )
        ]
        ([ h3 [ class "ma0 pl1" ] [ text ("Q" ++ (toString num) ++ " of 3") ]
         , p [ class "w-70 mv3 pl1" ] [ text filter_label ]
         ]
            ++ [ div
                    [ class
                        ("pv2 pl1 overflow-scroll h4"
                            ++ if (List.length tags) > 4 then
                                " mobile-scrollbars"
                               else
                                ""
                        )
                    ]
                    ([] ++ (List.map (\t -> render_tag_list t model.selected_tags num) tags))
               ]
            ++ [ div [ class "mt3 absolute bottom-1 w-100 ph4-ns ph1 left-0" ]
                    [ div [ class "w-50 dib tl" ]
                        [ previous_button num ]
                    , div [ class "w-50 dib tr" ]
                        [ next_button num ]
                    ]
               ]
            ++ [ div
                    [ class
                        ("absolute bottom-1 left-40 bg--lm-green pv2 ph4 b--lm-green ba"
                            ++ if model.results_updated /= num then
                                " dn"
                               else
                                ""
                        )
                    ]
                    [ text "Results Updated" ]
               ]
        )


render_tag_list : String -> List Tag -> Int -> Html Msg
render_tag_list tag selected_tags num =
    div [ class "dib" ]
        [ button
            [ class ("b--lm-orange lm-bg-orange-hover ba br2 ph2 pv1 lh-tag dib mb1 pointer montserrat mr1 " ++ (getTagColour (create_tag num tag) selected_tags))
            , onClick (SelectTag (create_tag num tag))
            ]
            [ text tag ]
        ]


getPosition : Int -> String
getPosition pos =
    case pos of
        1 ->
            "l-12-ns r-0"

        2 ->
            "r-50-ns r-115"

        3 ->
            "r-112-ns r-230"

        _ ->
            "l-12-ns"


getTagColour : Tag -> List Tag -> String
getTagColour tag selected_tags =
    if List.member tag selected_tags then
        "lm-bg-orange"
    else
        "lm-bg-light-orange"


create_tag : Int -> String -> Tag
create_tag num name =
    case num of
        1 ->
            Tag "q1" name

        2 ->
            Tag "q2" name

        3 ->
            Tag "q3" name

        _ ->
            Tag "q1" name


is_active : Model -> Int -> Bool
is_active model pos =
    model.tag_position == pos


get_active : Model -> Int -> String
get_active model pos =
    if (is_active model pos) then
        ""
    else
        "inactive"


previous_button : Int -> Html Msg
previous_button pos =
    case pos of
        1 ->
            text ""

        _ ->
            button
                [ class "tl dib bn bg-white pointer"
                , onClick (ResultsLoadingAlert pos (pos - 1))
                ]
                [ div [ class "v-mid h2 br-100 w2 pa1 mr2 dib next_left" ] []
                , div [ class "dib montserrat fw6 w-50 w-auto-ns" ] [ text "previous question" ]
                ]


next_button : Int -> Html Msg
next_button pos =
    case pos of
        3 ->
            button [ class "f5 link dib ph3 pv2 br1 pointer nunito tracked inner-shadow-active lm-white lm-bg-dark-turquoise lm-bg-white-hover lm-dark-turquoise-hover b--lm-dark-turquoise ba" ] [ a [ class "link", href "#results" ] [ text "Search" ] ]

        _ ->
            button
                [ class "tr dib bn bg-white pointer"
                , onClick (ResultsLoadingAlert pos (pos + 1))
                ]
                [ div [ class "dib montserrat fw6 w-50 w-auto-ns" ] [ text "next question" ]
                , div [ class "v-mid h2 br-100 w2 pa1 ml2 dib next_right" ] []
                ]
